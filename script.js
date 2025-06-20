console.log('Сайт Vibe-2 успешно загружен!'); 

let camera, scene, renderer;
let objects = [];
let raycaster;
let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false;
let canJump = false;
let velocity = new THREE.Vector3();
let direction = new THREE.Vector3();
let prevTime = performance.now();
let yaw = 0, pitch = 0;

const blocker = document.getElementById('blocker');
const instructions = document.getElementById('instructions');

init();
// Сразу убираем блокер и активируем управление
blocker.style.display = 'none';
animate();

function init() {
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.set(0, 10, 0);
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x222233);
    scene.fog = new THREE.Fog(0x222233, 0, 750);

    // Свет
    const light = new THREE.HemisphereLight(0xffffff, 0x444444);
    light.position.set(0, 200, 0);
    scene.add(light);

    // Плоскость (земля)
    const floorGeometry = new THREE.PlaneGeometry(2000, 2000, 100, 100);
    const floorMaterial = new THREE.MeshPhongMaterial({ color: 0x999999, depthWrite: false });
    const floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.rotation.x = -Math.PI / 2;
    scene.add(floor);

    // Препятствия
    const boxGeometry = new THREE.BoxGeometry(20, 20, 20);
    for (let i = 0; i < 20; i++) {
        const boxMaterial = new THREE.MeshPhongMaterial({ color: 0x8888ff });
        const box = new THREE.Mesh(boxGeometry, boxMaterial);
        box.position.x = Math.random() * 1600 - 800;
        box.position.y = 10;
        box.position.z = Math.random() * 1600 - 800;
        scene.add(box);
        objects.push(box);
    }

    // Цель
    const targetGeometry = new THREE.SphereGeometry(5, 32, 32);
    const targetMaterial = new THREE.MeshPhongMaterial({ color: 0xff2222 });
    const target = new THREE.Mesh(targetGeometry, targetMaterial);
    target.position.set(0, 5, -50);
    scene.add(target);
    objects.push(target);

    // Рендерер
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Клавиши
    document.addEventListener('keydown', function(event) {
        switch (event.code) {
            case 'ArrowUp':
            case 'KeyW': moveForward = true; break;
            case 'ArrowLeft':
            case 'KeyA': moveLeft = true; break;
            case 'ArrowDown':
            case 'KeyS': moveBackward = true; break;
            case 'ArrowRight':
            case 'KeyD': moveRight = true; break;
            case 'Space':
                if (canJump === true) velocity.y += 350;
                canJump = false;
                break;
        }
    });
    document.addEventListener('keyup', function(event) {
        switch (event.code) {
            case 'ArrowUp':
            case 'KeyW': moveForward = false; break;
            case 'ArrowLeft':
            case 'KeyA': moveLeft = false; break;
            case 'ArrowDown':
            case 'KeyS': moveBackward = false; break;
            case 'ArrowRight':
            case 'KeyD': moveRight = false; break;
        }
    });

    // Мышь — поворот камеры
    document.addEventListener('mousemove', function(event) {
        // Только при зажатой левой кнопке мыши
        if (event.buttons !== 1) return;
        yaw -= event.movementX * 0.002;
        pitch -= event.movementY * 0.002;
        pitch = Math.max(-Math.PI/2, Math.min(Math.PI/2, pitch));
    });

    // Стрельба
    document.addEventListener('mousedown', function (event) {
        if (event.button === 0) shoot();
    });

    raycaster = new THREE.Raycaster();
    window.addEventListener('resize', onWindowResize);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function shoot() {
    // Луч из центра экрана
    const directionVector = new THREE.Vector3(0, 0, -1).applyEuler(new THREE.Euler(pitch, yaw, 0, 'YXZ'));
    raycaster.set(camera.position, directionVector);
    const intersects = raycaster.intersectObjects(objects, false);
    if (intersects.length > 0) {
        const obj = intersects[0].object;
        if (obj.geometry.type === 'SphereGeometry') {
            obj.material.color.set(0x00ff00);
            setTimeout(() => obj.material.color.set(0xff2222), 500);
        }
    }
}

function animate() {
    requestAnimationFrame(animate);
    const time = performance.now();
    const delta = (time - prevTime) / 1000;
    velocity.x -= velocity.x * 10.0 * delta;
    velocity.z -= velocity.z * 10.0 * delta;
    velocity.y -= 9.8 * 100.0 * delta; // гравитация
    direction.z = Number(moveForward) - Number(moveBackward);
    direction.x = Number(moveRight) - Number(moveLeft);
    direction.normalize();
    if (moveForward || moveBackward) velocity.z -= direction.z * 400.0 * delta;
    if (moveLeft || moveRight) velocity.x -= direction.x * 400.0 * delta;
    // Перемещение камеры
    const forward = new THREE.Vector3(Math.sin(yaw), 0, Math.cos(yaw));
    const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw));
    camera.position.addScaledVector(forward, -velocity.z * delta);
    camera.position.addScaledVector(right, -velocity.x * delta);
    camera.position.y += velocity.y * delta;
    if (camera.position.y < 10) {
        velocity.y = 0;
        camera.position.y = 10;
        canJump = true;
    }
    // Поворот камеры
    camera.rotation.set(pitch, yaw, 0, 'YXZ');
    prevTime = time;
    renderer.render(scene, camera);
} 