import React, { useState } from 'react'
import lupa from '../assets/lupa.png'
import seta from '../assets/seta.png'
import '../CSS/filtro.css'

function Filtro() {

    const [ativo, setAtivo] = useState(false)

    const handleClick = () => {
        setAtivo(prev => !prev)
    }

  return (
    <>
      <div className="filtro_container">
        <div className="filtro_content">
            <form action="" method="get" className="filtro_formulario">
                <div className="filtro_principal">
                    <div className="filtro_input-generico">
                        <img src={lupa} id="btnBusca" alt="Buscar"/>
                        <input type="text" id="txtBusca" placeholder="Buscar endereço"/>
                    </div>
                    <button type="button" onClick={handleClick} className={`filtro_avancado ${ativo ? 'active' : ''}`}>
                        <p className="filtro_avancado-texto">Busca avançada</p>
                        <img className="filtro_avancado-seta" src={seta} alt="seta" />
                    </button>
                </div>
                <div className={`filtro_detalhado ${ativo ? 'active' : ''}`}>
                    <input className="filtro_medico" type="text" id="txtBusca" placeholder="Nome do Médico"/>
                    <input className="filtro_especialidade" type="text" id="txtBusca" placeholder="Especialidade"/>
                    <input className="filtro_convenio" type="text" id="txtBusca" placeholder="Convenio"/>
                </div>
            </form>
        </div>
      </div>
    </>
  )
}

export default Filtro
