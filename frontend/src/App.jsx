import {BrowserRouter as Router, Route,Routes} from 'react-router-dom'
import ProductList from './pages/ProductList.jsx';
import ProductDetails from './pages/ProductDetails.jsx';
import Navbar from './components/Navbar.jsx';
import CartPage from './pages/CartPage.jsx';
import CheckoutPage from './pages/CheckoutPage.jsx'
import Login from './pages/Login.jsx'
import Signup from './pages/Signup.jsx'
import PrivateRouter from './components/PrivateRouter.jsx'

function App() {
  return(
    <div>
      <Router>
        <Navbar/>
        <Routes>
          <Route path="/" element={<ProductList/>} />
          <Route path="/products/:id" element={<ProductDetails/>} />
          <Route path="/cart/" element={<CartPage/>} />
          <Route element={<PrivateRouter/>}>
              <Route path='/checkout' element={<CheckoutPage/>}/>
          </Route>
          <Route path='/login' element={<Login/>}/>
          <Route path='/signup' element={<Signup/>}/>

        </Routes>
      </Router>
    </div>
  )
}

export default App;