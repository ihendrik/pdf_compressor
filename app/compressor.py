import os, subprocess, shutil, glob, re

def find_ghostscript():
    gs = shutil.which("gswin64c.exe")
    if gs:
        return gs

    paths = glob.glob(r"C:\Program Files\gs\gs*\bin\gswin64c.exe")
    if paths:
        return sorted(paths)[-1]

    return None


def run_gs_with_progress(gs, inp, out, dpi, jpeg, percent_cb, cancel_flag):
    cmd = [
        gs,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dBATCH",

        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        "-dDetectDuplicateImages=true",

        "-dDownsampleColorImages=true",
        "-dDownsampleGrayImages=true",
        "-dDownsampleMonoImages=true",

        "-dColorImageDownsampleType=/Bicubic",
        "-dGrayImageDownsampleType=/Bicubic",
        "-dMonoImageDownsampleType=/Subsample",

        f"-dColorImageResolution={dpi}",
        f"-dGrayImageResolution={dpi}",
        f"-dMonoImageResolution={dpi}",

        "-dAutoFilterColorImages=true",
        "-dAutoFilterGrayImages=true",

        f"-dJPEGQ={jpeg}",

        f"-sOutputFile={out}",
        inp
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    total_pages = None
    total_pattern = re.compile(r"Processing pages \d+ through (\d+)")
    page_pattern = re.compile(r"Page\s+(\d+)")

    for line in process.stdout:
        line = line.strip()

        if total_pages is None:
            m = total_pattern.search(line)
            if m:
                total_pages = int(m.group(1))

        m = page_pattern.search(line)
        if m and total_pages:
            current = int(m.group(1))
            percent = int((current / total_pages) * 100)
            percent_cb(percent)

        if cancel_flag():
            process.terminate()
            return False

    process.wait()
    return process.returncode == 0


def size_mb(p):
    return os.path.getsize(p) / (1024 * 1024)

def safe_replace(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    os.rename(src, dst)

def compress_binary(gs, inp, out, max_size, bounds, iters,
                    log_cb, percent_cb, cancel_flag, iteration_cb):

    min_dpi, max_dpi, min_jpeg, max_jpeg = bounds

    tmp = os.path.join(os.path.dirname(out), "tmp.pdf")

    samples = []  # (f, size)

    best_file = None
    best_size = -1  # best under target

    closest_file = None
    closest_diff = float("inf")  # closest overall

    def run(f):
        dpi = int(min_dpi + (max_dpi - min_dpi) * f)
        jpeg = int(min_jpeg + (max_jpeg - min_jpeg) * f)

        log_cb(f"DPI={dpi} JPEG={jpeg}")

        ok = run_gs_with_progress(
            gs, inp, tmp, dpi, jpeg,
            percent_cb,
            cancel_flag
        )
        if not ok or not os.path.exists(tmp):
            return None

        s = size_mb(tmp)
        log_cb(f"→ {s:.2f} MB")
        return s

    # --- INITIAL PROBES ---
    for i, f in enumerate([0.0, 1.0]):
        iteration_cb(f"Init {i+1}/2")
        s = run(f)
        if s is None:
            continue

        samples.append((f, s))

        # track closest ALWAYS
        diff = abs(s - max_size)
        if diff < closest_diff:
            if closest_file and os.path.exists(closest_file):
                os.remove(closest_file)
            closest_file = tmp + ".closest.pdf"
            safe_replace(tmp, closest_file)
            closest_diff = diff
        else:
            os.remove(tmp)

        # track best under target
        if s <= max_size and s > best_size:
            if best_file and os.path.exists(best_file):
                os.remove(best_file)
            best_file = tmp + ".best.pdf"
            shutil.copy(closest_file, best_file)
            best_size = s

    # --- MAIN LOOP ---
    for i in range(iters):
        if cancel_flag():
            return False, None

        iteration_cb(f"Iteration {i+1}/{iters}")

        if len(samples) < 2:
            f = 0.5
        else:
            samples_sorted = sorted(samples, key=lambda x: x[1])

            below = [p for p in samples_sorted if p[1] <= max_size]
            above = [p for p in samples_sorted if p[1] > max_size]

            if below and above:
                f1, s1 = below[-1]
                f2, s2 = above[0]

                if s2 != s1:
                    f = f1 + (max_size - s1) * (f2 - f1) / (s2 - s1)
                else:
                    f = (f1 + f2) / 2
            else:
                f = sum(p[0] for p in samples) / len(samples)

        f = max(0.0, min(1.0, f))

        if any(abs(f - sf) < 0.01 for sf, _ in samples):
            f = (f + 0.5) / 2

        s = run(f)
        if s is None:
            continue

        samples.append((f, s))

        # --- track closest ALWAYS ---
        diff = abs(s - max_size)
        if diff < closest_diff:
            if closest_file and os.path.exists(closest_file):
                os.remove(closest_file)
            closest_file = tmp + ".closest.pdf"
            safe_replace(tmp, closest_file)
            closest_diff = diff
        else:
            os.remove(tmp)

        # --- track best under target ---
        if s <= max_size and s > best_size:
            if best_file and os.path.exists(best_file):
                os.remove(best_file)
            best_file = closest_file + ".best.pdf"
            shutil.copy(closest_file, best_file)
            best_size = s

        # --- convergence ---
        if best_size > 0 and abs(max_size - best_size) <= 0.5:
            log_cb(f"✔ Converged: {best_size:.2f} MB")
            break

    # --- FINAL OUTPUT ---
    if best_file and os.path.exists(best_file):
        os.rename(best_file, out)
        return True, best_size

    if closest_file and os.path.exists(closest_file):
        log_cb("⚠ Target unreachable, using closest result")
        os.rename(closest_file, out)
        return True, max_size + closest_diff

    return False, None