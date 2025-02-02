# save this as shell.nix
{ pkgs ? import <nixpkgs> {}}:

pkgs.mkShell {
  packages = [ pkgs.python312 pkgs.poetry ];

  shellHook = ''
    echo "Please use poetry shell to activate the virtual environment"
  '';
}


