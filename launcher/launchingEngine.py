import subprocess

def launchExecutable(executable):

    app = subprocess.run(
        ["launcher/launchingEngine.exe", executable],
        capture_output=True,
        text=True
    )

    print("STDOUT:", repr(app.stdout))
    print("STDERR:", repr(app.stderr))

    app_id = app.stdout.strip()

    print("APP ID:", repr(app_id))

    subprocess.run(
        ["explorer.exe", "shell:AppsFolder" + app_id]
    )

    return app_id
