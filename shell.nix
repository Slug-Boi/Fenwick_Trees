# save this as shell.nix
{ pkgs ? import <nixpkgs> {}}:

pkgs.mkShell {
  packages = [ pkgs.python312 ];

  shellHook = ''
    echo "--* Shell and conda env activated *--"
  '';
}


