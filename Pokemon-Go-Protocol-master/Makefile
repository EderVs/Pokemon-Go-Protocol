.PHONY : instructions clean run_client run_server man_pokemon_server man_pokemon_client create_manuals remove_manuals

instructions:
	@echo "make prepare-dev"
	@echo "         Prepara el entorno de desarrollo de la aplicación"
	@echo "		(Se necesita ejecutar con el comando sudo.)"
	@echo "		(Usar solo una vez.)"
	@echo "make man_pokemon_server"
	@echo "		Muestra el manual para el servidor"
	@echo "make man_pokemon_client"
	@echo "		Muestra el manual para el cliente"
	@echo "make create_manuals"
	@echo "		Instala los manuales del proyecto en el sistema."
	@echo "		(Se necesita ejecutar con el comando sudo.)"
	@echo "make remove_manuals"
	@echo "		Desinstala los manuales generados por el proyecto."
	@echo "		(Se necesita ejecutar con el comando sudo.)"
	@echo "make clean"
	@echo "		Borra los archivos generados por el proyecto."
	@echo "make run_client"
	@echo "		Ejecuta el cliente de Pokemón."
	@echo "make run_server"
	@echo "		Ejecuta el servidor de Pokemón."

install :
	apt-get -y install python3.6 python3-pip
	echo OK;

man_pokemon_server:
	@man ./manpages/pokemon_server

man_pokemon_client:
	@man ./manpages/pokemon_client

create_manuals:
	cp manpages/pokemon_server /usr/local/share/man/man1/pokemon_server.1
	gzip /usr/local/share/man/man1/pokemon_server.1 
	cp manpages/pokemon_client /usr/local/share/man/man1/pokemon_client.1 
	gzip /usr/local/share/man/man1/pokemon_client.1 
	echo Se han agregado los manuales 

remove_manuals:
	rm -f /usr/local/share/man/man1/pokemon_server.1.gz
	rm -f /usr/local/share/man/man1/pokemon_client.1.gz

run_client :	
	@if [ ! -d "./src/client_pokemons" ]; then \
		mkdir ./src/client_pokemons; \
	fi
	@cd src  && python3 client.py
run_server:
	@cd src && python3 server.py
clean:
	rm -f -r ./src/client_pokemons
	@echo Se borraron las imagenes descargadas de los pokemons.
