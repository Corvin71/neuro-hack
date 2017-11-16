var container, stats;
var camera, scene, renderer;
var controls;
var plane;
var targetRotation = 0;
var targetRotationOnMouseDown = 0;
var mouseX = 0;
var mouseXOnMouseDown = 0;
var windowHalfX = window.innerWidth / 2;

// Параметры в окошке по умолчанию
var params = {
    Радиатор: 0.5,      // крутилка батареи
    Кондиционер: 0.5,    // крутилка кондёра
    Человек_внутри: true,       // присутствие человека
    Length: 5,
    Width: 5
};

init();
animate();

function init() {
    CreateDiv();
    CreateCamera();

    scene = new THREE.Scene();
    scene.background = new THREE.Color( 0xf0f0f0 );
    
    // Axis Helper. Раскомментировать, если забуем,
    // куда направлены оси (гыы)
    //var axis = THREE.AxisHelper(200);
    //scene.add(axis);

    // Cube
    CreateRoom(0,0,0);
    /*
    CreateRoom(200,0,0);
    CreateRoom(0,0,150);
    CreateRoom(0,-100,0);
    */
    // Lightning - ЭТО МОЛНИЯ, БЛ*ТЬ!
    CreateLight();

    // Plane
    var geometry = new THREE.PlaneBufferGeometry( 1, 1 );
    geometry.rotateX( - Math.PI / 2 );
    var material = new THREE.MeshBasicMaterial( { color: 0xf2f7ff, overdraw: 0.5 } );
    plane = new THREE.Mesh( geometry, material );
    scene.add( new THREE.AmbientLight( 0xFFFFFF ) );
    scene.add( plane );

    // Загрузчик модели

    /**/var mtlLoader = new THREE.MTLLoader();
    mtlLoader.setPath( './models/' );
    mtlLoader.load('3d-mode3l.mtl', function (materials) {
        materials.preload();

        var radiatorLoader = new THREE.OBJLoader();
        radiatorLoader.setMaterials(materials);

        radiatorLoader.load('./models/3d-model3.obj', function(radiator) {

            scene.add(radiator);
        }, onProgress, onError);
    }, onProgress, onError);


    var manager = new THREE.LoadingManager();
    manager.onProgress = function( item, loaded, total ) {
        console.log( item, loaded, total );
    };

    var onProgress = function( xhr ) {
        if ( xhr.lengthComputable ) {
            var percentComplete = xhr.loaded / xhr.total * 100;
            console.log( Math.round( percentComplete, 2 ) + '% downloaded' );
        }
    };

    var onError = function( xhr ) {
        console.error( xhr );
    };

    /**/var radiator = new THREE.FBXLoader(manager);
    radiator.load( './models/radiator.FBX', function( object ) {
        object.scale.set(0.08, 0.08, 0.08);

        object.position.y = 20;
        object.position.x = -93;
        object.position.z = 40;
        object.rotation.z = Math.PI / 2;
        object.rotation.x = Math.PI / 2;

        scene.add( object );
    }, onProgress, onError);

    //Кондиционер, ибо я думаю про другой перевод...
    /*var condition = new THREE.FBXLoader(manager);
    condition.load( './models/AirCon.FBX', function( object ) {
        object.scale.set(0.08, 0.08, 0.08);

                object.position.y = 20;
                object.position.x = -93;
                object.position.z = 40;
                object.rotation.z = Math.PI / 2;
                object.rotation.x = Math.PI / 2;

        scene.add( object );
    }, onProgress, onError);
*/

    //Тут окно...
    /*var mtlLoader = new THREE.MTLLoader();
    mtlLoader.setPath( './models/' );
    mtlLoader.load('Window.mtl', function (materials) {
        materials.preload();

        var windowLoader = new THREE.OBJLoader();
        windowLoader.setMaterials(materials);

        windowLoader.load('./models/Window.obj', function(window) {
            window.scale.set(5, 5, 5);

            window.position.y = 20;
            //window.position.x = -93;
            window.position.z = 40;
            //window.rotation.z = Math.PI / 2;
            //window.rotation.x = Math.PI / 2;

            scene.add(window);
        }, onProgress, onError);
    }, onProgress, onError);*/

    //ДВЕРЬ БЛЯТЬ
    /*var doorLoader = new THREE.OBJLoader();
    var mat = new THREE.MeshBasicMaterial( { color: 0xf2f7ff, overdraw: 0.5 } );
    //doorLoader.setMaterials(mat);

    doorLoader.load('./models/3d-model2.fbx', function(door) {
        door.scale.set(3, 3, 4);

        door.position.y = 20;
        //window.position.x = -93;
        door.position.z = 40;
        //window.rotation.z = Math.PI / 2;
        //window.rotation.x = Math.PI / 2;

        scene.add(door);
    }, onProgress, onError);
*/

    // Установки рендера
    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    renderer.gammaInput = true;
    renderer.gammaOutput = true;
    renderer.shadowMap.enabled = true;

    // Установка поворота камеры по движению мыши
    controls = new THREE.OrbitControls(camera, renderer.domElement);

    // Окошко интерфейса
    var gui = new dat.GUI();
    gui.add(params, 'Радиатор', 0, 1);
    gui.add(params, 'Кондиционер', 0, 1);
    gui.add(params, 'Человек_внутри', [true, false]);

    gui.open();
    container.appendChild( renderer.domElement );
}


function animate() {
    requestAnimationFrame( animate );
    controls.update();
    renderer.render( scene, camera );
}


function CreateDiv() {
    container = document.createElement( 'div' );
    document.body.appendChild( container );
    var info = document.createElement( 'div' );
    info.style.position = 'absolute';
    info.style.top = '10px';
    info.style.width = '100%';
    info.style.textAlign = 'center';
    container.appendChild( info );
}

function CreateCamera() {
    camera = new THREE.PerspectiveCamera(30, window.innerWidth / window.innerHeight, 0.1, 10000);
    camera.position.y = 400;
    camera.position.z = 300;
    camera.lookAt(0, 0, 0);
}

function CreateRoom(rX, rY, rZ) {
    //Задняя стена.
    CreateObjectWall({Ox: rX, Oy: rY + 50, Oz: rZ - 75.5, angleX: 0, angleY: 0, angleZ: Math.PI, width: 200, height: 100, depth: 5, is_floor: false});
    //Пол.
    CreateObjectWall({Ox: rX, Oy: rY, Oz: rZ, angleX: Math.PI / 2, angleY: 0, angleZ: Math.PI / 2, width: 156, height: 200, depth: 5, is_floor: true});
    //Передняя стена.
    CreateObjectWall({Ox: rX, Oy: rY + 50, Oz: rZ + 75.5, angleX: 0, angleY: 0, angleZ: Math.PI, width: 200, height: 100, depth: 5, is_floor: false});
    //Левая стена.
    CreateObjectWall({Ox: rX + 97.5, Oy: rY + 50, Oz: rZ, angleX: 0, angleY: 0, angleZ: Math.PI, width: 5, height: 100, depth: 156, is_floor: false});
    //Правая стена.
    CreateObjectWall({Ox: rX - 97.5, Oy: rY + 50, Oz: rZ, angleX: 0, angleY: 0, angleZ: Math.PI, width: 5, height: 100, depth: 156, is_floor: false});
}


function CreateObjectWall(stat) {
    var geometry = new THREE.BoxGeometry(stat.width, stat.height, stat.depth);
    var upWallColor = 0xE9E9E9;
    var faceWallColor = 0xFFFFFF;
    var assWallColor = 0xAAAAAA;
    
    if(stat.is_floor) {
        var texture = new THREE.TextureLoader().load("./textures/hardwood2_diffuse.jpg");
        var material = new THREE.MeshStandardMaterial({
            map: texture,
            overdraw: true
        });
    }
    else {
        var material = new THREE.MeshStandardMaterial({
            color: assWallColor
        });
    }
    var cube = new THREE.Mesh( geometry, material );
    cube.position.x = stat.Ox;
    cube.position.y = stat.Oy;
    cube.position.z = stat.Oz;

    cube.rotation.x =  stat.angleX;
    cube.rotation.y = stat.angleY;
    cube.rotation.z = stat.angleZ;

    cube.receiveShadow = true;

    scene.add(cube);
}

function CreateLight() {
    // Свет! Озарил мою больную душу...
    light = new THREE.DirectionalLight(0xffffff, 2);
    light.position.set(0, 200, 120);
    light.castShadow = true;
    scene.add(light);
}
