{
  pkgs,
  lib,
  config,
  ...
}:
{
  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    version = "3.13";
  };

  # https://devenv.sh/packages/
  packages = [
    config.languages.python.package.pkgs.pyqt6
  ];

  # See full reference at https://devenv.sh/reference/options/
}














































