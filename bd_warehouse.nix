{ lib
, python
, buildPythonPackage
, fetchFromGitHub
, build123d
, setuptools
, setuptools_scm
}:
buildPythonPackage rec {
  pname = "bd_warehouse";
  version = "0.2.0";
  src = fetchFromGitHub {
    owner = "gumyr";
    repo = "bd_warehouse";
    rev = "v${version}";
    sha256 = "sha256-4M5UtVuH44wK4kmMVstdpiEBFzxkgNCK6Vsv3mqDcy0=";
  };

  build-system = [ setuptools setuptools_scm ];

  format = "pyproject";

  propagatedBuildInputs = [ build123d ];

  doCheck = false;
}
