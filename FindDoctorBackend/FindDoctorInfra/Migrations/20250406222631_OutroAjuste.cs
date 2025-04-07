using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace FindDoctorInfra.Migrations
{
    /// <inheritdoc />
    public partial class OutroAjuste : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Profissionais_Especialidades_EspecialidadeId",
                table: "Profissionais");

            migrationBuilder.AddForeignKey(
                name: "FK_Profissionais_Especialidades_EspecialidadeId",
                table: "Profissionais",
                column: "EspecialidadeId",
                principalTable: "Especialidades",
                principalColumn: "Id");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Profissionais_Especialidades_EspecialidadeId",
                table: "Profissionais");

            migrationBuilder.AddForeignKey(
                name: "FK_Profissionais_Especialidades_EspecialidadeId",
                table: "Profissionais",
                column: "EspecialidadeId",
                principalTable: "Especialidades",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
