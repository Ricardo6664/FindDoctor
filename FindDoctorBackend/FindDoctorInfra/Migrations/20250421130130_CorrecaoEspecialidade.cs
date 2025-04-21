using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace FindDoctorInfra.Migrations
{
    /// <inheritdoc />
    public partial class CorrecaoEspecialidade : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "EspecialidadeId",
                table: "ProfissionalEstabelecimentos",
                type: "text",
                nullable: true);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "EspecialidadeId",
                table: "ProfissionalEstabelecimentos");
        }
    }

}
