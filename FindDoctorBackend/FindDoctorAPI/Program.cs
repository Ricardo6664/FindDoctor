using FindDoctorDomain.Interfaces;
using FindDoctorInfra.Data;
using FindDoctorApplication.Services;
using FindDoctorInfra.HostedServices;
using FindDoctorInfra.Processadores;
using FindDoctorInfra.Repositories;
using FindDoctorInfra.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection"), npgsqlOptions => npgsqlOptions.UseNetTopologySuite()));

builder.Services.AddCors(options =>
{
    options.AddPolicy("PermitirFrontend", policy =>
    {
        policy
            .WithOrigins("http://localhost:5173")
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});

// Add services to the container.
builder.Services.AddScoped<IGeocodingService, PhotonGeocodingService>();
builder.Services.AddScoped<ImportacaoCnesService>();
builder.Services.AddScoped<AddressAppService>();
builder.Services.AddHostedService<ImportaCnesHostedService>();
builder.Services.AddScoped<IEstabelecimentoRepository, EstabelecimentoRepository>();
builder.Services.AddScoped<IEspecialidadeRepository, EspecialidadeRepository>();
builder.Services.AddScoped<EstabelecimentoAppService>();
builder.Services.AddScoped<EspecialidadeAppService>();
//builder.Services.AddScoped<ICnesCsvProcessor, ProfissionalEstabelecimentoCsvProcessor>();

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseAuthorization();

app.UseCors("PermitirFrontend");

app.MapControllers();

app.Run();
