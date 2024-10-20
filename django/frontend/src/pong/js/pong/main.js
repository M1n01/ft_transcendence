export const PongMainEvent = new Event('PongMainEvent');
import * as THREE from 'three';
import crown_img from '../../assets//medal-crown-10328-gold.png';
//import default_font from '../../assets//helvetiker_bold.typeface.json';
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js';
//import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js';
//import Typeface from '../../assets/ZenOldMincho_Regular.json';
import Typeface from '../..//assets/Roboto_Medium_Regular.json';
//import { fetchAsForm } from '../../../spa/js/utility/fetch.js';
import { addScore } from './addScore.js';
//import { DefaultFont } from 'three/examples/fonts/helvetiker_bold.typeface.json';
import '../../scss/pong.scss';

const keys = {
  q: false,
  a: false,
  o: false,
  l: false,
};

document.addEventListener('PongMainEvent', function async() {
  let isGameRunning = false;
  console.log('start pong');

  const canvas_block = document.getElementById('pong-canvas-block');
  if (canvas_block == null) {
    return;
  }

  //isGameRunning = true;
  //const canvas_style = document.window.getComputedStyle(canvas_block);
  //const canvas_style = window.getComputedStyle(canvas_block);

  // サイズを指定
  //const width = 750;
  //const height = 460;

  const width = Number(canvas_block.offsetWidth);
  const height = Number(canvas_block.offsetHeight);
  const PADDDLE_X = 560;
  //const PADDDLE_X = (1 - width / height / 2) * height + height + 15;
  const CAMERA_Z = 500;
  const PADDLE_INIT_SPEED = 5;

  const area = {
    minX: -605,
    maxX: 605,
    minY: -370,
    maxY: 370,
  };

  //const vx = 5;
  //const vy = 5;
  let ball_velocity = new THREE.Vector3(3, 3, 0);
  let paddle_velocity = new THREE.Vector3(0, PADDLE_INIT_SPEED, 0);

  // レンダラーを作成
  const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector('#myCanvas'),
  });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(width, height);

  // シーンを作成
  const scene = new THREE.Scene();

  // カメラを作成
  const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
  camera.position.set(0, 0, CAMERA_Z);

  const texture = new THREE.TextureLoader().load(crown_img);
  // 箱を作成
  const ball_geometry = new THREE.SphereGeometry(10, 32, 16);
  //const material = new THREE.MeshStandardMaterial({ map: texture, color: 0xff00ff });
  const material = new THREE.MeshBasicMaterial({ map: texture, color: 0xffffff });
  const ball = new THREE.Mesh(ball_geometry, material);
  const ball_obj = new THREE.Box3().setFromObject(ball);

  const pl_geometry = new THREE.BoxGeometry(25, 135, 0);
  const pl_material = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const paddle_left = new THREE.Mesh(pl_geometry, pl_material);
  const paddle_left_obj = new THREE.Box3().setFromObject(paddle_left);

  const pr_geometry = new THREE.BoxGeometry(25, 135, 0);
  const pr_material = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const paddle_right = new THREE.Mesh(pr_geometry, pr_material);
  const paddle_right_obj = new THREE.Box3().setFromObject(paddle_right);

  const fontLoader = new FontLoader();
  const Ffont = fontLoader.parse(Typeface);

  class ObjectText {
    // コンストラクター
    constructor(string) {
      this.string = string;

      this.material = new THREE.MeshBasicMaterial({
        color: 0xff2222,
        side: THREE.DoubleSide,
        //transparent: true,
        wireframe: false,
      });
      this.Geotext;

      //this.Geotext = new THREE.Mesh(TextGeometry, this.material);
    }
    Hidden() {
      this.Geotext.position.set(-1000, -1000, -1000); // Meshの位置を設定
    }
    Appear() {
      this.Geotext.position.set(0, 0, 0); // Meshの位置を設定
    }

    CreatObject() {
      const TEXT = this.string;
      const shapes = Ffont.generateShapes(TEXT, 8); //文字サイズ
      const TextGeometry = new THREE.ShapeGeometry(shapes, 8);
      TextGeometry.computeBoundingBox();
      TextGeometry.center(); //Center the geometry based on the bounding box.
      this.Geotext = new THREE.Mesh(TextGeometry, this.material);

      this.Geotext.position.set(0, 0, 0); // Meshの位置を設定
      this.Geotext.scale.set(4, 4, 4); // Meshの拡大縮小設定

      //中央に表示する
      this.Geotext.name = 'SongText';
      scene.add(this.Geotext);
    }
  }

  const count3 = new ObjectText('3');
  const count2 = new ObjectText('2');
  const count1 = new ObjectText('1');
  count3.CreatObject();
  count2.CreatObject();
  count1.CreatObject();

  const startPong = async () => {
    isGameRunning = false;
    ball.position.set(-1000, -1000, -1000);
    let vx = getRandomArbitrary(3, 3.5);
    let vy = getRandomArbitrary(3, 3.5);
    const a = getRandomArbitrary(-1, 1);
    const b = getRandomArbitrary(-1, 1);

    is_left = false;
    if (a < 0) {
      vx = vx * -1;
      is_left = true;
    }
    if (b < 0) {
      vy = vy * -1;
    }
    //paddle_velocity = new THREE.Vector3(0, PADDLE_INIT_SPEED * vec, 0);
    ball_velocity = new THREE.Vector3(1 * vx, 1 * vy, 0);

    count3.Appear();
    count2.Hidden();
    count1.Hidden();
    setTimeout(() => {
      count3.Hidden();
      count2.Appear();
    }, 1000);
    setTimeout(() => {
      count2.Hidden();
      count1.Appear();
    }, 2000);
    setTimeout(() => {
      count1.Hidden();
      ball.position.set(0, 0, 0);
      isGameRunning = true;
    }, 3000);
  };

  const points_up = [];
  const points_down = [];

  let line_offset = 50;
  // 頂点座標の追加
  points_up.push(new THREE.Vector3(0, area.minY - 100, 0));
  points_up.push(new THREE.Vector3(0, -line_offset, 0));
  points_down.push(new THREE.Vector3(0, area.maxY + 100, 0));
  points_down.push(new THREE.Vector3(0, line_offset, 0));

  // ジオメトリとマテリアルの生成
  let lineGeometryUp = new THREE.BufferGeometry().setFromPoints(points_up);
  const whiteMaterial = new THREE.LineDashedMaterial({
    color: 0xffffff,
    dashSize: 1,
    gapSize: 1,
  });
  let lineGeometryDown = new THREE.BufferGeometry().setFromPoints(points_down);
  //const whiteMaterialDown = new THREE.LineBasicMaterial({ color: 0xffffff });

  // 線オブジェクトを生成してシーンに追加する
  const line_up = new THREE.Line(lineGeometryUp, whiteMaterial);
  const line_down = new THREE.Line(lineGeometryDown, whiteMaterial);
  line_up.computeLineDistances();
  line_down.computeLineDistances();
  scene.add(line_up);
  scene.add(line_down);

  scene.add(ball);
  scene.add(paddle_left);
  scene.add(paddle_right);

  paddle_left.position.x = -PADDDLE_X;
  paddle_right.position.x = PADDDLE_X;
  paddle_left.position.y = 0;
  paddle_right.position.y = 0;

  const ball_position = async (ball) => {
    ball.rotation.y += 0.1;
    ball.rotation.x += 0.1;
    ball.position.add(ball_velocity);

    if (
      (area.minX - 100 <= ball.position.x && ball.position.x <= area.minX) ||
      (ball.position.x >= area.maxX && ball.position.x <= area.maxX + 100)
    ) {
      isGameRunning = false;
      await addScore(ball, area);
      await startPong();
    }
    if (ball.position.y <= area.minY || ball.position.y >= area.maxY) {
      ball_velocity.y = -ball_velocity.y; // y方向の速度を反転
    }
    return ball;
  };

  // キーボードイベントの設定
  document.addEventListener('keydown', (event) => {
    if (event.key in keys) {
      keys[event.key] = true;
    }
  });

  document.addEventListener('keyup', (event) => {
    if (event.key in keys) {
      keys[event.key] = false;
    }
  });

  function paddle_position(paddle, is_left) {
    if (is_left) {
      if (keys['a'] && paddle.position.y > area.minY) paddle.position.y -= paddle_velocity.y;
      if (keys['q'] && paddle.position.y < area.maxY) paddle.position.y += paddle_velocity.y;
    } else {
      if (keys['l'] && paddle.position.y > area.minY) paddle.position.y -= paddle_velocity.y;
      if (keys['o'] && paddle.position.y < area.maxY) paddle.position.y += paddle_velocity.y;
    }
  }

  let is_left = false;

  function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
  }

  startPong();
  tick();
  function tick() {
    if (isGameRunning) {
      count3.Hidden();
      count2.Hidden();
      count1.Hidden();

      ball_position(ball);
      paddle_position(paddle_left, true);
      paddle_position(paddle_right, false);

      ball_obj.setFromObject(ball);
      paddle_left_obj.setFromObject(paddle_left);
      paddle_right_obj.setFromObject(paddle_right);

      if (ball_obj.intersectsBox(paddle_left_obj) && is_left) {
        is_left = false;

        ball_velocity.x = Math.abs(ball_velocity.x) + 1;
        ball_velocity.y = getRandomArbitrary(
          -Math.abs(ball_velocity.x * 2),
          Math.abs(ball_velocity.x) * 2
        );
      }
      if (ball_obj.intersectsBox(paddle_right_obj) && !is_left) {
        is_left = true;
        ball_velocity.x = -(Math.abs(ball_velocity.x) + 1);
        ball_velocity.y = getRandomArbitrary(
          -Math.abs(ball_velocity.x * 2),
          Math.abs(ball_velocity.x) * 2
        );
      }
    }
    renderer.render(scene, camera);
    requestAnimationFrame(tick);
  }
});
