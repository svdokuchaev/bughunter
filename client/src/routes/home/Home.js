/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-present Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React from 'react';
import PropTypes from 'prop-types';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import s from './Home.css';
import Graph from '../../components/Graph';

class Home extends React.Component {
  static propTypes = {
    news: PropTypes.arrayOf(
      PropTypes.shape({
        title: PropTypes.string.isRequired,
        link: PropTypes.string.isRequired,
        content: PropTypes.string,
      }),
    ).isRequired,
  };

  render() {
    return (
        <div className={s.root}>
      			<div className={s.header}>
      				<div className={s.top}>
      						<nav className={s.nav}>
                    <div className={s.nav_box}>
                      <h3 className={s.nav_box__title}>Title</h3>
                      <div className={s.nav_box__text}>aksfjalskfjalsfjalsfkajsf</div>
                      <div><img className={s.nav_box__image} src="https://placeimg.com/1000/1000/any" /></div>
                    </div>
                    <div className={s.nav_box}>
                      <h3 className={s.nav_box__title}>Title</h3>
                      <div className={s.nav_box__text}>aksfjalskfjalsfjalsfkajsf</div>
                      <div><img className={s.nav_box__image} src="https://placeimg.com/1000/1000/any" /></div>
                    </div>
                    <div className={s.nav_box}>
                      <h3 className={s.nav_box__title}>Title</h3>
                      <div className={s.nav_box__text}>aksfjalskfjalsfjalsfkajsf</div>
                      <div><img className={s.nav_box__image} src="https://placeimg.com/1000/1000/any" /></div>
                    </div>
                    <div className={s.nav_box}>
                      <h3 className={s.nav_box__title}>Title</h3>
                      <div className={s.nav_box__text}>aksfjalskfjalsfjalsfkajsf</div>
                      <div><img className={s.nav_box__image} src="https://placeimg.com/1000/1000/any" /></div>
                    </div>
                    <div className={s.nav_box}>
                      <h3 className={s.nav_box__title}>Title</h3>
                      <div className={s.nav_box__text}>aksfjalskfjalsfjalsfkajsf</div>
                      <div>
                        <img className={s.nav_box__image} src="https://placeimg.com/1000/1000/any" />
                      </div>
                    </div>
      						</nav>
      				</div>
      				<div className={s.bottom}>
      				</div>
      			</div>
      			<div className={s.main}>
      					<section id="top" className={[s.one, s.dark, s.cover].join(' ')}>
      						<div className={s.container}>
      								<h2 className={s.alt}><strong>BUGHUNTER</strong></h2>
      						</div>
      					</section>
      					<section id="portfolio" className={s.two}>
      						<div className={s.container}>
      							<header>
      								<h2>Graph</h2>
      							</header>
      							<p>Vitae natoque dictum etiam semper magnis enim feugiat convallis convallis
      							egestas rhoncus ridiculus in quis risus amet curabitur tempor orci penatibus.
      							Tellus erat mauris ipsum fermentum etiam vivamus eget. Nunc nibh morbi quis
      							fusce hendrerit lacus ridiculus.</p>
      						</div>
                  <Graph />
      					</section>
      			</div>
      			<div id={s.footer}>
      					<ul className={s.copyright}>
      						<li>&copy; Untitled. All rights reserved.</li><li>Design: <a href="http://html5up.net">HTML5 UP</a></li>
      					</ul>
      			</div>
            <script src="//cdnjs.cloudflare.com/ajax/libs/d3/4.1.1/d3.min.js"></script>
          </div>
    );
  }
}

export default withStyles(s)(Home);
