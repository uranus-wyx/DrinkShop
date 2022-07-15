import { BrowserRouter as Router , Routes, Route} from 'react-router-dom'
import Home from './components/pages/Home';
import About from './components/pages/About';
import NotFound from './components/pages/NotFound';

import Item from './components/pages/Item';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import Alert from './components/layout/Alert';

import { AlertProvider } from './context/alert/AlertContext';
import { ShopProvider } from './context/shop/ShopContext';

function App() {
  return (
    <ShopProvider>
      <AlertProvider>
        <Router basename="/shop">
            <div className="flex flex-col justify-between h-screen">
            <Navbar />

            <main className='container mx-auto px-3 pb-12'>
                <Alert />
                <Routes>
                <Route path='/' element={<Home />} />
                <Route path='/about' element={<About />} />
                <Route path='/item/:itemid' element={<Item />} />
                <Route path='/notfound' element={<NotFound />} />
                <Route path='/*' element={<NotFound />} />

                </Routes>
            </main>
            <Footer />
            </div>
        </Router>
      </AlertProvider>
    </ShopProvider>
  );
}

export default App;
