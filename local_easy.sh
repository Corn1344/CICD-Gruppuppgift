#!/bin/bash
./build.sh
./pytest.sh
./test_lint.sh
./deploy.sh
./curltests.sh
