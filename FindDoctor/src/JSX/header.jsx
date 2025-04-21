import '../CSS/header.css'
import logo from '../assets/localmed_logo.jpg'

function Header() {

  return (
    <>
      <div className="header_container">
        <div className="header_content">
            <a href="./" className="header_logo">
                <img src={logo} alt="Logo LocalMed" className="Logo" />
            </a>
        </div>
      </div>
    </>
  )
}

export default Header