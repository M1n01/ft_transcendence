
import * as THREE from 'three'

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
	canvas: document.getElementById('canvas'),
  // antialias: true,
});

renderer.setSize(window.innerWidth, window.innerHeight);

//game objs

const paddleGeometry = new THREE.BoxGeometry(10, 100, 10);
const paddleMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
const paddle1 = new THREE.Mesh(paddleGeometry, paddleMaterial);
const paddle2 = new THREE.Mesh(paddleGeometry, paddleMaterial);

const ballGeometry = new THREE.SphereGeometry(10, 32, 32);
const ballMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
const ball = new THREE.Mesh(ballGeometry, ballMaterial);

const wallGeometry = new THREE.BoxGeometry(10, 10, 10);
const wallMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
const topWall = new THREE.Mesh(wallGeometry, wallMaterial);
const bottomWall = new THREE.Mesh(wallGeometry, wallMaterial);
const leftWall = new THREE.Mesh(wallGeometry, wallMaterial);
const rightWall = new THREE.Mesh(wallGeometry, wallMaterial);

scene.add(paddle1, paddle2, ball, topWall, bottomWall, leftWall, rightWall);


let ballVelocity = new THREE.Vector3(0.5, 0.5, 0);
let paddle1Velocity = 0;
let paddle2Velocity = 0;

function update() {
  ball.position.x += ballVelocity.x;
  ball.position.y += ballVelocity.y;

  if (ball.position.y > 490 || ball.position.y < -490) {
    ballVelocity.y = -ballVelocity.y;
  }
  if (ball.position.x > 490 || ball.position.x < -490) {
    ballVelocity.x = -ballVelocity.x;
  }

  if (ball.position.x < -440 && ball.position.y > paddle1.position.y - 50 && ball.position.y < paddle1.position.y + 50) {
    ballVelocity.x = -ballVelocity.x;
  }
  if (ball.position.x > 440 && ball.position.y > paddle2.position.y - 50 && ball.position.y < paddle2.position.y + 50) {
    ballVelocity.x = -ballVelocity.x;
  }

  paddle1.position.y += paddle1Velocity;
  paddle2.position.y += paddle2Velocity;

  renderer.render(scene, camera);
}

setInterval(update, 16); // 60 FPS

document.addEventListener('keydown', (event) => {
  switch (event.key) {
    case 'ArrowUp':
      paddle1Velocity = -5;
      break;
    case 'ArrowDown':
      paddle1Velocity = 5;
      break;
    case 'w':
      paddle2Velocity = -5;
      break;
    case 's':
      paddle2Velocity = 5;
      break;
  }
});

document.addEventListener('keyup', (event) => {
  switch (event.key) {
    case 'ArrowUp':
    case 'ArrowDown':
      paddle1Velocity = 0;
      break;
    case 'w':
    case 's':
      paddle2Velocity = 0;
      break;
  }
});
