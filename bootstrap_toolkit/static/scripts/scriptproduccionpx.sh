#! /bin/bash
#######################################
### Script para levantar el servidor###
### Grupo R05: 	Juan Duarte	    ###
### 		Carlos Riquelme	    ###
###		Gerardo Riveros	    ###
#######################################
clear

######################################
###Comprobar todas las dependencias###
######################################
echo 'comprobamos e instalamos pip'
sleep 1s
sudo apt-get install python-pip
sudo pip install django-dajax django-dajaxice
sudo pip install django-admin-bootstrapped
sudo pip install reportlab
sudo pip install pydot
#Creamos el entorno virtual
clear
echo 'Instalamos lo necesario para el entorno Virtual'
sleep 1s
sudo pip install virtualenvwrapper

export WORKON_HOME=$HOME/entornoVirtual/
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv entornoIS2

clear
echo 'instalando Django'
sleep 1s
#instalamos Django especihttps://github.com/amigleon92/ProyectoIS2.gitfico
pip install django==1.6.2

clear
echo 'instalando postgres'
sleep 1s
#instalamos postgres
sudo apt-get install libpq-dev python-dev
sudo apt-get install postgresql postgresql-contrib

clear
echo 'instalando librerias'
sleep 1s
#instalamos el conector de la basde de datos con django
pip install psycopg2

#instalamos la libreria para Paths
pip install unipath

#desactivamos el entorno virtual
deactivate

########################################
### Instalamos los servidores ##########
########################################
clear
echo 'instalando apache'
sleep 1s
#instalamos apache
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
sudo service apache2 restart

clear
echo 'instalando repositorio'
sleep 1s
#instalamos el repositorio 
sudo apt-get install git
sudo apt-get install xclip

#comprobamos la version
git --version
sleep 1s

clear
echo 'configurando el repositorio'
sleep 1s
#asociamos el usuario
#git config --global user.name "gerardoriveros"
#git config --global user.email "gerardojriveros@gmail.com"

#iniciamos el git
git init
git clone https://github.com/JuanBer90/ProjectX.git

echo 'copiamos el entorno al proyecto'
sleep 1s
#copiamos el entorno a el proyecto
rm -rf $HOME/PycharmProjects/ProjectX
cp -R $HOME/entornoVirtual/ProjectX $HOME/PycharmProjects/ProjectX

cd $HOME/PycharmProjects/
#ir a la carpeta del proyecto e iniciar el entorno virtual
######################################
###Hacemos el menu para los tag#######
######################################
clear
osch=0
echo "1. iteracion 1"
echo "2. iteracion 2"
echo "3. iteracion 3"
echo "4. iteracion 4"
echo "5. iteracion 5"
echo "6. iteracion 6"
echo "7. iteracion 7"
echo -n "Seleccione la iteracion a descargar [1 al 7]? "
read osch

if [ $osch -eq 1 ] ; then
	echo "iteracion 1"
	sleep 1s
	git checkout a7dc856d28f0c236ffbdd59f7a46321015acb16f
	clear
	sleep 1s
	sudo -u postgres dropdb projectxDB
	clear
	echo 'creando la base de datos'
	sudo -u postgres createdb projectxDB --owner=postgres

elif [ $osch -eq 2 ]
then
	echo "iteracion 2"
	sleep 1s
	git checkout 1f001f8a869511bc72131aa74e0cfda83b4b5925
	clear
	echo 'creando la base de datos'
	sleep 1s
	sudo -u postgres dropdb projectxDB
	sudo -u postgres createdb projectxDB --owner=postgres

elif [ $osch -eq 3 ]
then
	echo "iteracion 3"
	sleep 1s
	git checkout 8370aa17024fbff595f5fccaa2ef9a74b675de2e
	clear
	echo 'creando la base de datos'
	sleep 1s
	sudo -u postgres dropdb projectxDB
	sudo -u postgres createdb projectxDB --owner=postgres

elif [ $osch -eq 4 ]
then
	echo "iteracion 4"
	sleep 1s
	git checkout 41f64ca8eb2bfffee173ce57e3c4e4697ee84152
	clear
	sleep 1s
	echo 'creando la base de datos'
	sleep 1s
	sudo -u postgres dropdb projectxDB
	sudo -u postgres createdb projectxDB --owner=postgres

elif [ $osch -eq 5 ]
then
	echo "iteracion 5"
	sleep 1s
	git checkout 174bef222387b533756a8fc6dddd0d1cf3f9eb9a
	clear
	echo 'creando el usuario produccion, ingrese password: produccion'
	sleep 1s
	sudo -u postgres drobdb projectxDB
	sudo -u postgres createdb projectxDB -- owner=postgres

elif [ $osch -eq 6 ]
then
	echo "iteracion 6"
	sleep 1s
	git checkout 02b48794c95538b74127db82611a6df80f20cdca
	sleep 1s
	clear
	echo 'creando la base de datos'
	sleep 1s
	sudo -u postgres dropdb projectxDB
	sudo -u postgres createdb projectxDB --owner=postgres

elif [ $osch -eq 7 ]
then
	echo "iteracion 7"
	sleep 1s
	git checkout 6fa431315110bca7dd7d97c9f314421e83a5bcfd
	sleep 1s
	clear
	echo 'creando la base de datos'
	sleep 1s
	sudo -u postgres dropdb projectxDB
	sudo -u postgres createdb projectxDB --owner=postgres

else
	echo "Ultimo Commit"
	sleep 1s
	echo 'creando el usuario produccion, ingrese password: produccion'
	sleep 1s
	echo "Poblamos la base de Datos"
	psql -f $HOME//PycharmProjects/ProjectX/bootstrap_toolkit/static/scripts/poblado_tabkas_desarrollo.backup projectXDB -h localhost -U postgres -W

fi

echo 'activa el entorno'
sleep 1s
source entornoIS2/bin/activate
#sincronizar la base de datos
python manage.py syncdb
sleep 1s

#desactivamos el entorno virtual
deactivate
echo 'movemos el servidor a lugar que debe estar'
sleep 1s
sudo mkdir /var/www/
sudo rm -rf /var/www/ProjectX/
cd $HOME
sudo mv -f -v $HOME/PycharmProjects/ProjectX/ /var/www/ProjectX/


####################################################
###### Configuracion de apache #####################
####################################################
echo 'configurando apache'
sleep 1s

sudo mkdir /var/www/html/
sudo mv -v /var/www/index.html /var/www/html/
sudo mv /etc/apt/apt.conf /var/www/html
sudo cp $HOME//PycharmProjects/ProjectX/bootstrap_toolkit/static/scripts/apt.conf /etc/apt/
echo 'reiniciamos apache'
sleep 1s
sudo /etc/init.d/apache2 restart

clear
sudo apt-get install libgnome2-bin
clear
echo 'abriendo el navegador'
echo '.'
echo '..'
echo '...'
sleep 1s
gnome-open http://localhost
