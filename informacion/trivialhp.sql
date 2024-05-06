CREATE DATABASE `TrivialHP`;
Use `TrivialHP`;
CREATE TABLE `Trivial_preguntas_generales_HP`(
 `id` TINYINT (2) NOT NULL,
`pregunta` VARCHAR (200) NOT NULL,
`respuesta_correcta` VARCHAR (200) NOT NULL,
`respuesta_incorrecta1` VARCHAR (200) NOT NULL,
` respuesta_incorrecta2` VARCHAR (200) NOT NULL,
` respuesta_incorrecta3` VARCHAR (200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Resultados_HP_TEST`(
 	`id` TINYINT (2) NOT NULL,
`nombre` VARCHAR (100) NOT NULL,
`aciertos` TINYINT (2)  NULL,
`errores` TINYINT (2)  NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `estudiantes_casas`(
 	`id` TINYINT (2) NOT NULL,
`casa` VARCHAR (30) NOT NULL,
`numEstudiantes` INT (10) NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


 
INSERT INTO Trivial_preguntas_generales_HP VALUES
(1,'¿Cómo se llaman los padres de Harry Potter?','James y Lilly','Jhon y Lilly', 'Robert y Martha','James y Lissie'),
(2,'¿Cómo se llama la lechuza de Harry Potter?', 'Hedwig', 'Errol', 'Pigwidgeon','Herwin'),
(3,'¿Cómo se llama la rata de Ron Weasley?', 'Scabbers', 'Jerry', 'Splinter','Scooter'),
(4,'¿ Cómo se llama el gato de Hermione Granger?', 'Crookshanks', 'Garfield', 'Félix','Shanks'),
(5,'¿Cómo se llama la rana de Neville Longbotton a lo largo de las películas de Harry Potter?', 'Trevor', 'Jean-Bob', 'Reborn','Tina'),
(6,'¿Qué actor interpreta al personaje de Cedric Digory en la cuarta película de Harry Potter', ' Robert Pattinson', 'Robert Parkinson', 'Henry Cavill','Mattew Lewis'),
(7,'¿Quién el padre de Draco Malfoy?', 'Lucius Malfoy', 'Lucas Malfoy', 'Damian Malfoy', 'Abraxas Malfoy'),
(8,'¿Quién es el Príncipe Mestizo?', 'Severus Snape', 'Harry Potter', 'Lily Potter', 'Neville Longbottom'),
(9,'¿Qué actriz interpreta a Bellatrix Lestrange?', 'Helena Bonham Carter', 'Beatrix Bonham Carley', 'Helen MCCrory','Maggie Smith'),
(10,'¿Qué hechizo usó Harry para matar a Lord Voldemort?', 'Expelliarmus', 'Avada Kedavra', 'Sectumsempra','Rictusempra'),
(11,'¿Qué nombres recibían los miembros del grupo de James Potter en Hogwarts?',' Los merodeadores', 'Los rondadores', 'Los aulladores', 'Los animagos'),
(12,'¿Cómo se llama el padre de Luna Lovegood?', 'Xenophilius Lovegood', 'Warlocks Lovegood', 'Prophesied Lovegood', 'Hocus Lovegood'),
(13,'¿Cuál fue el motivo del juramento inquebrantable entre Severus Snape y Narcisa Malfoy en la sexta película de Harry Potter?', 'Proteger a Draco Malfoy en su misión', 'Evitar que Draco Malfoy cumpliera su misión', 'Expulsar a Harry Potter de Howgarts', 'Construir un armario mágico'),
(14,'¿Qué criaturas invisibles tiran de las carrozas en Hogwarts?', 'Thestrals', 'Abraxans', 'Bicornios', 'Hipogrifos'),
(15,'¿Qué personas pueden ver las criaturas Thestrals?', 'Aquellos que han presenciado la muerte', 'Todos los magos', 'Los magos de alto nivel, como los aurores', 'Únicamente se pueden ver si se toma una poción'),
(16,'¿Cómo se llama el conductor del autobus noctámbulo que aparece en la tercera película de Harry Potter?', 'Ernie', 'Arnold', 'Robert', 'Otto'),
(17,'¿Cuál es el nombre del primer duende que recibe a Harry Potter en el banco de Gringotts?', 'Griphook', 'Bogrod', 'Ragnuk', 'Gringott'),
(18,'¿Qué criatura es Aragog en el mundo mágico de Harry Potter?', 'Acromántula', 'Atlach-Nacha', 'Ella.Laraña', 'Charlotte'),
(19,'¿Cómo se llama el fiel compañero y perro de Hagrid?', 'Fang', 'Sam', 'Gus', 'Slinky'),
(20,'¿El hechizo `Felifors` convierte a un animal en un qué?', 'Caldero', 'Rata', 'Flor', 'Cáliz'),
(21,'¿Las lágrimas de qué animal son el único antídoto conocido contra el veneno de basilisco?', 'Fénix', 'Unicornio', 'Mandrágora', 'Banshee'),
(22,'¿Cuál de los siguientes hechiceros fue uno de los fundadores de Hogwarts?', 'Rowena Ravenclaw', 'Cedric Gryffindor', 'Samuel Slytherin', 'Hugh Hufflepuff'),
(23,'¿Quién mato al elfo Dobby con un cuchillo en la primera parte de Harry Potter y las relíquias de la muerte?', 'Bellatrix Lestrange', 'Alecto Carrow', 'Peter Pettigrew', 'Lucius Malfoy'),
(24,' ¿De qué actor estuvo Emma Watson profundamente enamorada a lo largo de la saga de Harry Potter?', ' Tom Felton', 'Matthew Lewis', 'Daniel Radcliffe', 'Robert Pattinson'),
(25,' ¿En qué posición juega Harry en su equipo de Quidditch?', 'Buscador', 'Guardián', 'Golpeador', 'Cazador'),
(26, '¿Qué requisito puso JK Rowling al equipo de producción de Harry Potter a la hora de escoger el reparto de las películas?', 'Todos tenían que ser de origen británico', 'Al menos la mitad del reparto debía ser pelirrojo', 'Todos debían de haberse leído todos los libros publicados hasta la fecha', 'Ninguno'),
(27, '¿Qué hechizo se utiliza para desarmar a otro mago?', 'Expeliarmus', 'Confundus', 'Accio', 'Crucio'),
(28,'¿De qué está hecha la varita de Harry Potter?', 'Pluma de Fénix', 'Pelo de cola de unicornio', 'Corazón de dragon', 'Cuerno de basilisco'),
(29,'¿Qué forma animal tiene el patronous de Luna Lovegood?', 'Marmota', 'Nutria', 'Conejo','Perro'),
(30,'¿Cuándo se publicó el primer libro de Harry Potter?', '1997', '1990', '1992', '1989'),
(31,'¿Cuándo se estrenó la primera película de Harry Potter?', '2001','1999','2000','2005'),
(32, '¿Qué debe decir el usuario del Mapa del Merodeador después de usarlo para restablecerlo?', 'Travesura realizada', 'Maximum secretus', 'Epoximise', 'Nox'),
(33,'¿Cómo se le ocurrió la idea de Harry Potter a su escritora JK Rowling?', 'En un viaje en tren hacia Londres', 'Un día de excursión en el Zoo', 'Tomando cervezas con sus amigos', 'Yendo al cine con sus hijos'),
(34,' ¿En qué calle de Inglaterra vive la família de los Dursley?', 'Nº4 Privet Drive', 'Nº10 Abbey Road', 'Nº34 Leicester Square', 'Nº56 Lombard Street'),
(35,'¿Qué planta ingiere Harry Potter en el lago negro para poder respirar bajo el agua en el torneo de los tres magos?', 'Branquialgas', 'Asfódelo', 'Acónito', 'Bubotubérculo'),
(36,'¿Qué nombre recibe el perro guardián de 3 cabezas?', 'Fluffy', 'Goofy', 'Puffy', 'Max'),
(37,'¿Qué instrumento mágico mantiene dormido al perro guardián de 3 cabezas?', 'Un arpa mágica', 'Una arpa mágica', 'Una radio', 'Un ukelele mágico'),
(38,'¿Cuántas escaleras tiene Hogwarts?', '142', '256', '77', '108'),
(39,'¿Qué se obtiene al ingerir la pócima Felix Felicis?', 'Tienes suerte durante 24 horas', 'Felicidad máxima', 'La muerte', 'Puedes transformarte en la persona que quieras'),
(40,'¿Cuál de los siguientes NO es un Horrocrux de Voldemort?', 'El espejo de Oesed', 'Un guardapelo', 'Nagini', 'Harry Potter'),
(41,'¿Cómo conseguía Hermione Granger atender a todas sus clases?', 'Viajando en el tiempo', 'Los profesores le pasan los apuntes de las clases que no pueda asistir', 'Recibe clases particulares', 'Se crea un clon que asiste en su lugar'),
(42,'¿Cómo caza Harry su primera Snitch?', 'Con la boca', 'Con la mano', 'Se le cuela en la capucha de la capa', 'No lo consiguen, pierden el primer partido'),
(43,'¿Quién se hace pasar por Ojo Loco Moody, el profesor de cuarto año de Defensa Contra las Artes Oscuras de Harry?', 'Barty Crouch Jr', 'Grogan Stump', 'Antonin Dolohov', 'Ludovic Bagman'),
(44, '¿Cuántas varitas rompió Daniel Radcliffe en el set al usarlas como baquetas de bateria?', '80', '3', '15', 'Ninguna'),
(45,'¿Cómo se llama el gigante medio hermano de Hagrid?', 'Grawp', 'Rubeus', 'Goldric', 'Sam'),
(46,'¿ A que mortífago suplanta la identidad Hermion para poder acceder a Gringotts?', 'Bellatrix Lestrange', 'Narcisa Malfoy', 'Alecto Carrow', 'Bertha Jokins'),
(47,' ¿Qué prenda le regalo Harry Potter a Dobby para ser libre?', 'Un calcetín', 'Una corbata', 'Un pañuelo', 'Una camiseta vieja'),
(48,' ¿Qué significan las iniciales R.A.B en el Horrocrux que guarda Albus Dumbledore?', 'Regulus Arcturus Black', 'Ronald Astrid Black', 'Rupert Albus Blame', 'Radley Albany Buster'),
(49,'¿Qué es “El Quisquilloso”?', 'Un periódico', 'Una golosina mágica', 'Un tipo de conjuro', 'Una poción'),
(50,'¿Qué nombre recibe la tienda de chucherías cerca de Hogwarts?', 'Honeydukes', 'Weasley&Weasley', 'Pettichaps', 'Flourish & Blotts');


INSERT INTO estudiantes_casas VALUES
(1,'Gryffindor',0),
(2,'Hufflepuff',0),
(3,'Ravenclaw',0),
(4,'Slytherin',0);