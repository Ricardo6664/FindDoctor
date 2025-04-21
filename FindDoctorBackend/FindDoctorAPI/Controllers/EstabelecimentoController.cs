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
        public async Task<IActionResult> BuscarProximos([FromQuery] string endereco, [FromQuery] double raioKm = 5)
        {
            var estabelecimentos = await _service.BuscarProximosAsync(endereco, raioKm);
            return Ok(estabelecimentos);
        }
    }
}
