{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    devShell.aarch64-linux = let
      pkgs = nixpkgs.legacyPackages.aarch64-linux;
    in pkgs.mkShell {
      packages = with pkgs; [ (python312.withPackages (ps: [ ps.pygame ps.numpy ps.pillow])) ];
    };
  };
}
