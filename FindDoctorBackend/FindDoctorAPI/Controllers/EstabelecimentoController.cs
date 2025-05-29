using FindDoctorDomain.Interfaces;
using FindDoctorApplication.Services;
using Microsoft.AspNetCore.Mvc;

namespace FindDoctorAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class EstabelecimentoController : ControllerBase
    {
        private readonly EstabelecimentoAppService _service;
        
        public EstabelecimentoController(EstabelecimentoAppService service)
        {
            _service = service;
        }

        [HttpGet("proximos")]
        public async Task<IActionResult> BuscarProximos(
            [FromQuery] double latitude,
            [FromQuery] double longitude,
            [FromQuery] double raioKm = 5,
            [FromQuery] string? especialidadeId = null,
            [FromQuery] string? nomeMedico = null,
            [FromQuery] int? convenioId = null
        )
        {
            var estabelecimentos = await _service.BuscarProximosAsync(
                latitude,
                longitude,
                raioKm,
                especialidadeId,
                nomeMedico,
                convenioId);

            return Ok(estabelecimentos);
        }

        [HttpGet("{codigoCNES}")]
        public async Task<IActionResult> BuscarPorCodigoCNES(string codigoCNES)
        {
            var estabelecimento = await _service.GetById(codigoCNES);

            if (estabelecimento == null)
                return NotFound();

            return Ok(estabelecimento);
        }
    }
}
