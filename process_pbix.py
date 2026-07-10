import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


def find_executable(paths):
    for path in paths:
        if os.path.isfile(path):
            return path
    return None


def get_default_downloads_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")


def select_pbix(downloads_dir):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        initialdir=downloads_dir,
        title="Selecione o PBIX baixado",
        filetypes=[("Power BI files", "*.pbix"), ("Todos os arquivos", "*")],
    )
    root.destroy()
    return file_path


def confirm_message(message):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo("Ação necessária", message)
    root.destroy()


def copy_to_repo(src_path, repo_dir):
    dest_path = os.path.join(repo_dir, os.path.basename(src_path))
    if os.path.exists(dest_path):
        print(f"O arquivo já existe em: {dest_path}")
        print("Ele será sobrescrito.")
    shutil.copy2(src_path, dest_path)
    return dest_path


def open_powerbi(pbix_path):
    possible_paths = [
        os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Microsoft Power BI Desktop", "bin", "PBIDesktop.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Microsoft Power BI Desktop", "bin", "PBIDesktop.exe"),
        os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Microsoft Power BI Desktop", "PBIDesktop.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Microsoft Power BI Desktop", "PBIDesktop.exe"),
    ]
    pbi_exe = find_executable(possible_paths)
    if pbi_exe:
        return subprocess.Popen([pbi_exe, pbix_path], shell=False)

    try:
        os.startfile(pbix_path)
        return None
    except OSError:
        return None


def open_github_desktop():
    possible_paths = [
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "GitHubDesktop", "GitHubDesktop.exe"),
        os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "GitHub Desktop", "GitHubDesktop.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "GitHub Desktop", "GitHubDesktop.exe"),
    ]
    gh_exe = find_executable(possible_paths)
    if gh_exe:
        try:
            subprocess.Popen([gh_exe], shell=False)
            return True
        except OSError:
            return False
    try:
        os.startfile("github-desktop://")
        return True
    except OSError:
        return False


def main():
    repo_dir = os.path.abspath(os.path.dirname(__file__))
    downloads_dir = get_default_downloads_folder()

    print("Abrindo seletor de arquivos na pasta Downloads...")
    pbix_path = select_pbix(downloads_dir)
    if not pbix_path:
        print("Nenhum PBIX selecionado. Encerrando.")
        sys.exit(1)

    print(f"Arquivo selecionado: {pbix_path}")
    dest_path = copy_to_repo(pbix_path, repo_dir)
    print(f"Arquivo copiado para o repositório: {dest_path}")

    print("Abrindo no Power BI Desktop...")
    pbi_proc = open_powerbi(dest_path)

    confirm_message(
        "O Power BI Desktop abriu o arquivo.\n\nClique em Salvar como → Projeto do Power BI.\n\nQuando terminar, feche o Power BI para continuar."
    )

    if pbi_proc is not None:
        pbi_proc.wait()
    else:
        input("Após fechar o Power BI Desktop, pressione Enter para continuar...")

    if os.path.exists(dest_path):
        try:
            os.remove(dest_path)
            print(f"PBIX excluído: {dest_path}")
        except OSError as err:
            print(f"Falha ao excluir o PBIX: {err}")
    else:
        print("O PBIX para exclusão não foi encontrado.")

    if open_github_desktop():
        print("GitHub Desktop aberto.")
    else:
        print("Não foi possível abrir o GitHub Desktop automaticamente.")

    commit_message = "baseline: sincroniza com versão publicada do Workspace"
    try:
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(commit_message)
        root.update()
        root.destroy()
        print("Mensagem de commit copiada para a área de transferência.")
    except Exception:
        print("Não foi possível copiar a mensagem para a área de transferência.")

    print("Sugestão de commit:")
    print(commit_message)
    print("Use este texto como mensagem de commit no GitHub Desktop.")


if __name__ == "__main__":
    main()
