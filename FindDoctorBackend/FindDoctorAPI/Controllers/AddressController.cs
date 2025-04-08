using Microsoft.AspNetCore.Mvc;
using FindDoctorApplication.Services;
using FindDoctorDomain.ValueObjects;

namespace FindDoctorAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AddressController : ControllerBase
    {
        private readonly AddressAppService _addressAppService;

        public AddressController(AddressAppService addressAppService)
        {
            _addressAppService = addressAppService;
        }

        [HttpGet("buscar")]
        public async Task<ActionResult<List<Address>>> BuscarEnderecos([FromQuery] string endereco)
        {
            if (string.IsNullOrWhiteSpace(endereco))
                return BadRequest("Endereço não pode estar vazio.");

            var resultado = await _addressAppService.BuscarCoordenadas(endereco);

            if (resultado == null || resultado.Count == 0)
                return NotFound("Nenhum endereço encontrado.");

            return Ok(resultado);
        }
    }
}
