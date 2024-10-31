{
  inputs = {
    cq-flake.url = "github:marcus7070/cq-flake";
    nixpkgs.follows = "cq-flake/nixpkgs";
  };

  outputs = { self, nixpkgs, cq-flake, ... } @ inputs:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        config.permittedInsecurePackages = [
          "freeimage-unstable-2021-11-01"
        ];
      };
      python = cq-flake.outputs.packages.${system}.python;
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          (python.withPackages (
            ps: with ps; [
              cadquery
              cq-kit
              pyright
              black
              mypy
            ]
          ))
        ];
      };
      apps = cq-flake.outputs.apps;
      packages = cq-flake.outputs.packages;
    };
}
