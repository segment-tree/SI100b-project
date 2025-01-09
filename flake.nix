{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  
  outputs = inputs @ {
    self,
    nixpkgs,
    flake-parts,
    ...
  } : flake-parts.lib.mkFlake { inherit inputs; } {
    flake = {
    };
    systems = [
      "x86_64-linux"
      "x86_64-darwin"
      "aarch64-linux"
      "aarch64-darwin"
    ];
    perSystem = { system, pkgs, ... }: let
      pkgs = import nixpkgs {
        inherit system;
      };
    in rec {
      packages.default = let
      # 定义 Python 环境
      pythonEnv = pkgs.python3Packages.buildPythonPackage {
        pname = "bubbles-valley";
        version = "0.0.2";

        # 设置项目源码目录
        src = ./.;
        # 引入 requirements.txt
        nativeBuildInputs = with pkgs; [ (python312.withPackages (ps: [ ps.pygame ps.openai ps.setuptools ])) ];
        propagateBuildInputs = with pkgs; [ (python312.withPackages (ps: [ ps.pygame ps.openai ps.setuptools ])) ];
        buildInputs = with pkgs; [ (python312.withPackages (ps: [ ps.pygame ps.openai ps.setuptools ])) ];
        installPhase = ''
          mkdir -p $out/bin
        '';

        # 测试代码运行
        doCheck = false;
        checkPhase = ''
          python -m unittest discover tests
        '';

        meta = with pkgs.lib; {
          description = "A Python project packaged with Flakes and requirements.txt";
          homepage = "https://github.com/user/my-python-project";
          license = licenses.mit;
          maintainers = [ maintainers.yourname ];
        };
      };
    in
      pythonEnv;
      apps.default = {
          type = "app";
          program = "${packages.default}/bin/main";
        };
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [ (python312.withPackages (ps: [ ps.pygame ps.openai ps.mypy ps.setuptools ps.pyinstrument])) ];
      };
    };
  };
}
