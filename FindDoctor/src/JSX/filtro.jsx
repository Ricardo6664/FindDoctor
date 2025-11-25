import React, { useState } from 'react'
import lupa from '../assets/lupa.png'
import seta from '../assets/seta.png'
import FiltroEspecialidade from './filtroEspecialidade'
import '../CSS/filtro.css'


function Filtro() {
  const [ativo, setAtivo] = useState(false);
  const [enderecoBusca, setEnderecoBusca] = useState("");
  const [sugestoes, setSugestoes] = useState([]);
  const [mostrarSugestoes, setMostrarSugestoes] = useState(false);
  const [enderecoSelecionado, setEnderecoSelecionado] = useState(null);
  const [nomeMedico, setNomeMedico] = useState("");
  const [especialidadeSelecionada, setEspecialidadeSelecionada] = useState(null);

  const handleClick = () => {
    setAtivo((prev) => !prev);
  };

  const buscarEndereco = async () => {
    if (!enderecoBusca.trim()) return;

    const url = `http://localhost:5210/api/Address/buscar?endereco=${encodeURIComponent(enderecoBusca)}`;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error("Erro ao buscar endereço");

      const data = await response.json();
      setSugestoes(data);
      setMostrarSugestoes(true);
    } catch (error) {
      console.error("Erro:", error.message);
    }
  };

  const formatarEndereco = (endereco) => {
  
    const partes = [
      endereco.name,
      endereco.street,
      endereco.district,
      endereco.city,
      endereco.county,
      endereco.state,
      endereco.postcode,
      endereco.country,
    ];

    const partesValidas = partes.filter(
      (parte) => parte && parte !== "null" && parte.trim() !== ""
    );

  
    return partesValidas.join(", ");
};

  const selecionarSugestao = (sugestao) => {
    setEnderecoBusca(formatarEndereco(sugestao));
    setEnderecoSelecionado(sugestao);
    setMostrarSugestoes(false);
  };

  
  const buscarEnderecoConfirmado = async () => {
    if (!enderecoSelecionado) {
      alert("Por favor, selecione um endereço válido.");
      return;
    }

    const { latitude, longitude } = enderecoSelecionado.location || {};

    if (latitude == null || longitude == null) {
      alert("Endereço selecionado não possui coordenadas válidas.");
      return;
    }

    const raioKm = 1;

    let url = `http://localhost:5210/api/Estabelecimento/proximos?latitude=${latitude}&longitude=${longitude}&raioKm=${raioKm}`;

    if (nomeMedico.trim() !== "") {
      url += `&nomeMedico=${encodeURIComponent(nomeMedico.trim())}`;
    }
    if (especialidadeSelecionada && especialidadeSelecionada.id) {
      url += `&especialidadeId=${encodeURIComponent(especialidadeSelecionada.id)}`;
    }

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error("Erro ao buscar estabelecimentos próximos");

      const data = await response.json();

      window.dispatchEvent(new CustomEvent('estabelecimentosAtualizados', { detail: data }));

    } catch (error) {
      console.error("Erro:", error.message);
    }
  };

  return (
    <div className="filtro_container">
      <div className="filtro_content">
        <form
          action=""
          method="get"
          className="filtro_formulario"
          onSubmit={(e) => e.preventDefault()}
        >
          <div className="filtro_principal">
            <div className="filtro_input-generico" style={{ position: "relative" }}>
              <img
                src={lupa}
                id="btnBusca"
                alt="Buscar"
                onClick={buscarEndereco}
                style={{ cursor: "pointer" }}
              />
              <input
                type="text"
                id="txtBuscaEndereco"
                placeholder="Buscar endereço"
                value={enderecoBusca}
                onChange={(e) => setEnderecoBusca(e.target.value)}
                onFocus={() => {
                  if (sugestoes.length > 0) setMostrarSugestoes(true);
                }}
                
              />
              {mostrarSugestoes && sugestoes.length > 0 && (
                <ul
                  className="sugestoes-lista"
                  style={{
                    position: "absolute",
                    top: "100%",
                    left: 0,
                    right: 0,
                    backgroundColor: "#fff",
                    border: "1px solid #ccc",
                    zIndex: 10,
                    listStyle: "none",
                    padding: 0,
                    margin: 0,
                    maxHeight: "200px",
                    overflowY: "auto",
                  }}
                >
                  {sugestoes.map((sugestao, index) => (
                    <li
                      key={index}
                      onClick={() => selecionarSugestao(sugestao)}
                      style={{
                        padding: "8px",
                        cursor: "pointer",
                        borderBottom: "1px solid #eee",
                      }}
                      onMouseDown={(e) => e.preventDefault()}
                    >
                      {formatarEndereco(sugestao)}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <button
              type="button"
              onClick={handleClick}
              className={`filtro_avancado ${ativo ? "active" : ""}`}
              style={{ marginLeft: "16px" }}
            >
              <p className="filtro_avancado-texto">Busca avançada</p>
              <img className="filtro_avancado-seta" src={seta} alt="seta" />
            </button>
          </div>

          <div className={`filtro_detalhado ${ativo ? "active" : ""}`}>
             <input
              className="filtro_medico"
              type="text"
              placeholder="Nome do Médico"
              value={nomeMedico}
              onChange={(e) => setNomeMedico(e.target.value)}
            />
            <FiltroEspecialidade
              onSelect={(esp) => setEspecialidadeSelecionada(esp)}
            />
            <input
              className="filtro_convenio"
              type="text"
              placeholder="Convenio"
            />
          </div>

          
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              marginTop: "8px",
            }}
          >
            <button
              type="button"
              onClick={buscarEnderecoConfirmado}
              style={{
                padding: "8px 16px",
                cursor: "pointer",
                backgroundColor: "#007bff",
                color: "#fff",
                border: "none",
                borderRadius: "4px",
                fontSize: "16px",
                zIndex: 1
              }}
            >
              Buscar endereço
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}


export default Filtro
