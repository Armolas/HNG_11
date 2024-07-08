#build_files.sh
sudo apt update
sudo apt install python3
python -m ensurepip --upgrade
pip install -r requirements.txt

# make migrations
python3 manage.py migrate 
python3 manage.py collectstatic

