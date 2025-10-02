import os, tempfile, requests, shutil, zipfile, tarfile

def download_pypi_sdist(pkgname, version=None, unzip=True, untar=True, extract_to=None, verbose=True):
    url = f"https://pypi.org/pypi/{pkgname}/json"
    if verbose:
        print(f"Got repository URL: {url}")
    r = requests.get(url)
    if r.status_code not in [200, 201, 202, 301, 302]:
        raise ValueError(f"Package '{pkgname}' returned error code {r.status_code}.")
    data = r.json()
    latest = version if version else data["info"]["version"]
    files = data["releases"][latest]
    sdist_url = None
    for f in files:
        if f["packagetype"] == "sdist":
            sdist_url = f["url"]
            if verbose:
                print(f"Found source dist URL: {sdist_url}")
            break
    if not sdist_url:
        raise ValueError("No source distribution (sdist) found.")
    if verbose:    
        print(f"Latest distribution found: {latest} (if enabled to be latest, installs latest)")    
    tmp_dir = tempfile.mkdtemp(prefix="pypi_download_")
    file_name = os.path.basename(sdist_url)
    file_path = os.path.join(tmp_dir, file_name)
    target_dir = extract_to or os.path.dirname(file_path)            
    os.makedirs(target_dir, exist_ok=True)   
    if verbose:
        print(f"Downloading {pkgname}=={latest} -> {os.path.join(target_dir, file_name)}")
    with requests.get(sdist_url, stream=True) as repository:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(repository.raw, f)
    if file_name.endswith(".zip") and unzip:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            unzipname = os.path.join(target_dir, os.path.splitext(os.path.basename(file_name))[0])
            for member in zip_ref.infolist():
                zip_ref.extract(member, unzipname)
                if verbose:
                  print(f"Unpacked: {member.filename}")

            
    elif file_name.endswith((".tgz", ".tar.gz")) and untar:
        with tarfile.open(file_path, "r:gz") as tgz_ref:
            untgzname = os.path.join(target_dir, os.path.splitext(os.path.splitext(os.path.basename(file_name))[0])[0])
            for member in tgz_ref.getmembers():
                if member.isfile():
                    tgz_ref.extract(member, untgzname, set_attrs=True)
                    if verbose:
                        print(f"Unpacked: {member.name}")

             
    if verbose:
        print(f"Download complete! File saved at: {file_path}")
    return file_path