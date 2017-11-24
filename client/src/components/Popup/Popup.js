import React from 'react';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import PropTypes from 'prop-types';
import s from './Popup.css';

class Popup extends React.Component {
  static propTypes = {
    title: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired,
  };
  constructor(props) {
    super(props)
  }
  onClose(e) {
    e.preventDefault();
    this.props.onPopupClose(true);
  }
  render() {
    const { title, text, hidden, onPopupClose } = this.props;
    return(
      <div id="popup1" className={s.overlay + (hidden ? "" : " " + s.overlay_opened )}>
      	<div className={s.popup}>
      		<h2>{title}</h2>
      		<a className={s.close} href="#" onClick={this.onClose.bind(this)}>&times;</a>
      		<div className={s.content}>
      			{text}
      		</div>
          <div className={s.image}>
            <img className={s.image__img} src="https://placeimg.com/1000/1000/any" />
          </div>
      	</div>
      </div>
    );
  }

  componentDidMount() {
    console.log(this)
  }
}

export default withStyles(s)(Popup);
