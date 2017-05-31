cd /home/deploy/GDELT/gdelt-keywords/ # cd to project root_path
. .venv/bin/activate # source python virtualenv for this project

python top100_keywords_dowloader.py
python scp_data_to_storage.py
