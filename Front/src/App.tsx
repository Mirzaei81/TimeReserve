import { Routes, Route } from 'react-router-dom';
import {Home} from "./Home"
import {Market} from "./Markets"
import Layout from "./Layout"
import {NoMatch} from "./NoMatch"
import "./App.css"
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import { prefixer } from 'stylis';
import rtlPlugin from 'stylis-plugin-rtl';
import { MarketDetail } from './MarketDetail';
import Success from './Success';

// Create rtl cache
const cacheRtl = createCache({
  key: 'muirtl',
  stylisPlugins: [prefixer, rtlPlugin],
});

function Rtl(props:any) {
  return <CacheProvider value={cacheRtl}>{props.children}</CacheProvider>;
}


export default function App() {
  return (
    <>
      <Rtl>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path='/market/' element={<Market />}/>
            <Route path='/market-detail/:id' element={<MarketDetail/>}/>
            <Route path='/success' element={<Success/>}/>
            <Route path="*" element={<NoMatch />} />
          </Route>
        </Routes>
      </Rtl>
    </>
  );
}
