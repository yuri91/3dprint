{ lib
, python
, buildPythonPackage
, fetchFromGitHub
, build123d
, setuptools
, setuptools_scm
}:
buildPythonPackage rec {
  pname = "cq-warehouse";
  rev = "c172b91e00ed9b5b0d14b486ce816b93e9ce6ff0";
  version = "0.1.0";
  src = fetchFromGitHub {
    owner = "gumyr";
    repo = "bd_warehouse";
    inherit rev;
    sha256 = "sha256-8ifYANm2qDX1JpmlC87T8aEBACoiJyorXjwc8z9WqJU=";
  };

  build-system = [ setuptools setuptools_scm ];

  format = "pyproject";

  propagatedBuildInputs = [ build123d ];

  checkPhase = ''
    ${python.interpreter} -m unittest tests
  '';
}
