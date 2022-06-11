#!bin/sh 
dirname="passworder_test"

if [ ! -d $dirname ];
then
	git clone https://github.com/Rac-Software-Development/fastapi_passworder.git passworder_test;
fi


cd passworder_test;

pip install -r requirements.txt --upgrade;

python3 -m unittest discover . ;

if [ $? -eq 0 ];
then
  echo "Tests ran well..."
else
  echo "exit code: $?"
  exit 1;
fi

cd passworder;
git describe --tags > version.txt;

cd ../../;

mv ./passworder_test passworder;

cd passworder;

python3 main.py;
