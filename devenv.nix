{
  pkgs,
  lib,
  config,
  ...
}:
{
  # https://devenv.sh/packages/
  packages = [
  (pkgs.python312.withPackages (ps: [
    ps.pyqt6
  ]))
    pkgs.pywal
    pkgs.imagemagick
    pkgs.qt6.qtwayland
  ];

  env = {
    QT_QPA_PLATFORM = "wayland";
    QT_PLUGIN_PATH = "${pkgs.qt6.qtwayland}/lib/qt-6/plugins";
  };
  /*
  packages = with pkgs; [
    pywal
    imagemagick
    python3Packages.pyqt6
    qt6.qtwayland
  ]; */

  # https://devenv.sh/languages/
  #languages.python.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}

