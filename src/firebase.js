import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyCljP-42cACEmRS0BVWlBsULqJ1M6WvZ0U",
  authDomain: "miniminds-21663.firebaseapp.com",
  projectId: "miniminds-21663",
  storageBucket: "miniminds-21663.appspot.com",
  messagingSenderId: "818795651571",
  appId: "1:818795651571:web:ebb4d1f14e5993e7c27286",
  measurementId: "G-T52QQ74T0H"
};
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();
export { auth, provider };
