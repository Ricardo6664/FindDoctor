using FindDoctorDomain.Interfaces;
using FindDoctorApplication.Services;
using Microsoft.AspNetCore.Mvc;

namespace FindDoctorAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class EspecialidadeController: ControllerBase
    {
        private readonly EspecialidadeAppService _service;
        
        public EspecialidadeController(EspecialidadeAppService service)
        {
            _service = service;
        }

        [HttpGet("")]
        public async Task<IActionResult> GetAll()
        {
            var especialidades = await _service.GetAll();

            return Ok(especialidades);
        }
    }
}
