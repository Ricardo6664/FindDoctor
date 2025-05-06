using Microsoft.EntityFrameworkCore.Migrations;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

#nullable disable

namespace FindDoctorInfra.Migrations
{
    /// <inheritdoc />
    public partial class moreTables : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Id",
                table: "Profissionais");

            migrationBuilder.DropColumn(
                name: "SUS",
                table: "Estabelecimentos");

            migrationBuilder.CreateTable(
                name: "Convenios",
                columns: table => new
                {
                    Id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    Nome = table.Column<string>(type: "text", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Convenios", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "EstabelecimentoComProfissional",
                columns: table => new
                {
                    CodigoCNES = table.Column<string>(type: "text", nullable: false),
                    Nome = table.Column<string>(type: "text", nullable: false),
                    CNPJ = table.Column<string>(type: "text", nullable: false),
                    Endereco = table.Column<string>(type: "text", nullable: false),
                    Numero = table.Column<string>(type: "text", nullable: false),
                    Bairro = table.Column<string>(type: "text", nullable: false),
                    Cidade = table.Column<string>(type: "text", nullable: false),
                    UF = table.Column<string>(type: "text", nullable: false),
                    Latitude = table.Column<double>(type: "double precision", nullable: false),
                    Longitude = table.Column<double>(type: "double precision", nullable: false),
                    Telefone = table.Column<string>(type: "text", nullable: false),
                    CO_Profissional = table.Column<string>(type: "text", nullable: true),
                    NomeProf = table.Column<string>(type: "text", nullable: true),
                    CNS = table.Column<string>(type: "text", nullable: true),
                    SUS = table.Column<bool>(type: "boolean", nullable: true),
                    EspecialidadeId = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                });

            migrationBuilder.CreateTable(
                name: "EstabelecimentosConvenios",
                columns: table => new
                {
                    CodigoCNES = table.Column<string>(type: "text", nullable: false),
                    ConvenioId = table.Column<int>(type: "integer", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_EstabelecimentosConvenios", x => new { x.CodigoCNES, x.ConvenioId });
                    table.ForeignKey(
                        name: "FK_EstabelecimentosConvenios_Convenios_ConvenioId",
                        column: x => x.ConvenioId,
                        principalTable: "Convenios",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_EstabelecimentosConvenios_Estabelecimentos_CodigoCNES",
                        column: x => x.CodigoCNES,
                        principalTable: "Estabelecimentos",
                        principalColumn: "CodigoUnidade",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_EstabelecimentosConvenios_ConvenioId",
                table: "EstabelecimentosConvenios",
                column: "ConvenioId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "EstabelecimentoComProfissional");

            migrationBuilder.DropTable(
                name: "EstabelecimentosConvenios");

            migrationBuilder.DropTable(
                name: "Convenios");

            migrationBuilder.AddColumn<int>(
                name: "Id",
                table: "Profissionais",
                type: "integer",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<bool>(
                name: "SUS",
                table: "Estabelecimentos",
                type: "boolean",
                nullable: false,
                defaultValue: false);
        }
    }
}
