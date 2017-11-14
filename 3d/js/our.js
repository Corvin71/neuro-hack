var container, stats;
var camera, scene, renderer;
var controls;
var plane;
var targetRotation = 0;
var targetRotationOnMouseDown = 0;
var mouseX = 0;
var mouseXOnMouseDown = 0;
var windowHalfX = window.innerWidth / 2;

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
    CreateRoom(200,0,0);
    CreateRoom(0,0,150);
    CreateRoom(0,-100,0);
    
    // Lightning
    CreateLight();

    // Plane
    var geometry = new THREE.PlaneBufferGeometry( 1, 1 );
    geometry.rotateX( - Math.PI / 2 );
    var material = new THREE.MeshBasicMaterial( { color: 0xf2f7ff, overdraw: 0.5 } );
    plane = new THREE.Mesh( geometry, material );
    scene.add( new THREE.AmbientLight( 0xFFFFFF ) );
    scene.add( plane );

    // Загрузчик модели
    var radiatorLoader = new THREE.OBJLoader();
    radiatorLoader.load('./models/radiators.obj', function(radiator) {
        scene.add(radiator);
    });

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    renderer.gammaInput = true;
    renderer.gammaOutput = true;
    renderer.shadowMap.enabled = true;

    controls = new THREE.OrbitControls(camera, renderer.domElement);

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
    CreateObjectWall({Ox: rX + 0, Oy: rY + 50, Oz: rZ - 75.5, angleX: 0, angleY: 0, angleZ: Math.PI, width: 200, height: 100, depth: 5, is_floor: false});
    //Пол.
    CreateObjectWall({Ox: rX + 0, Oy: rY, Oz: rZ, angleX: Math.PI / 2, angleY: 0, angleZ: Math.PI / 2, width: 156, height: 200, depth: 5, is_floor: true});
    //Передняя стена.
    CreateObjectWall({Ox: rX + 0, Oy: rY + 50, Oz: rZ + 75.5, angleX: 0, angleY: 0, angleZ: Math.PI, width: 200, height: 100, depth: 5, is_floor: false});
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
