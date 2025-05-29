import React, { useState, useEffect, useRef } from 'react'

export default function FiltroEspecialidade({ onSelect }) {
  const [termo, setTermo] = useState('')
  const [opcoes, setOpcoes] = useState([])
  const [listaCompleta, setListaCompleta] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState(null)
  const [showDropdown, setShowDropdown] = useState(false)
  const containerRef = useRef(null)

  useEffect(() => {
    setCarregando(true)
    fetch('http://localhost:5210/api/Especialidade')
      .then(res => {
        if (!res.ok) throw new Error('Erro ao buscar especialidades')
        return res.json()
      })
      .then(data => {
        setListaCompleta(data)
        setOpcoes(data)
        setCarregando(false)
      })
      .catch(e => {
        setErro(e.message)
        setCarregando(false)
      })
  }, [])

  useEffect(() => {
    if (!termo) {
      setOpcoes(listaCompleta)
      return
    }
    const filtrado = listaCompleta.filter(e =>
      e.nome.toLowerCase().includes(termo.toLowerCase())
    )
    setOpcoes(filtrado)
  }, [termo, listaCompleta])

  useEffect(() => {
    function handleClickFora(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setShowDropdown(false)
      }
    }
    document.addEventListener('mousedown', handleClickFora)
    return () => document.removeEventListener('mousedown', handleClickFora)
  }, [])

  const selecionar = (especialidade) => {
    setTermo(especialidade.nome)
    setShowDropdown(false)
    if (onSelect) onSelect(especialidade)
  }

  return (
    <div ref={containerRef} style={{ position: 'relative', width: '250px' }}>
      <input
        className="filtro_especialidade"
        type="text"
        placeholder="Especialidade"
        value={termo}
        onChange={e => {
            const valor = e.target.value
            setTermo(valor)
            setShowDropdown(true)

            if (valor.trim() === '' && onSelect) {
                onSelect(null) 
            }
        }}
        onFocus={() => setShowDropdown(true)}
        autoComplete="off"
      />
      {showDropdown && (
        <div
          style={{
            position: 'absolute',
            background: 'white',
            border: '1px solid #ccc',
            maxHeight: '150px',
            overflowY: 'auto',
            width: '100%',
            zIndex: 1000,
          }}
        >
          {carregando && <div style={{ padding: '8px' }}>Carregando...</div>}
          {erro && <div style={{ padding: '8px', color: 'red' }}>{erro}</div>}
          {!carregando && !erro && opcoes.length === 0 && (
            <div style={{ padding: '8px' }}>Nenhuma especialidade encontrada.</div>
          )}
          {!carregando &&
            !erro &&
            opcoes.map((e) => (
              <div
                key={e.id}
                onClick={() => selecionar(e)}
                style={{
                  padding: '8px',
                  cursor: 'pointer',
                  borderBottom: '1px solid #eee',
                }}
                onMouseDown={e => e.preventDefault()}
              >
                {e.nome}
              </div>
            ))}
        </div>
      )}
    </div>
  )
}
