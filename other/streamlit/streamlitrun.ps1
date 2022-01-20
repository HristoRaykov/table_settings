$MAIN_DIR_PATH = (Get-Item $PSScriptRoot).Parent.FullName
$SOURCE_ROOT_DIR_NAME = "web"
$PYTHON_FILE_NAME = "streamlit_demo.py"
$SOURCE_ROOT_PATH = Join-Path $MAIN_DIR_PATH $SOURCE_ROOT_DIR_NAME
$FULL_PATH = Join-Path $SOURCE_ROOT_PATH $PYTHON_FILE_NAME

$env:PYTHONPATH += $MAIN_DIR_PATH

$PYTHON_ENV_NAME = "findata"
conda activate $PYTHON_ENV_NAME

Set-Location $SOURCE_ROOT_PATH

streamlit run $FULL_PATH

#start -WindowStyle Hidden