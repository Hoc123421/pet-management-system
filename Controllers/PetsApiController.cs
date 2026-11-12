using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PetManagement.Data;
using PetManagement.Models;
using System.Linq;
using System.Threading.Tasks;

namespace PetManagement.Controllers
{
    [ApiController]
    [Route("api/pets")]
    public class PetsApiController : ControllerBase
    {
        private readonly PetDbContext _context;

        public PetsApiController(PetDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<IActionResult> GetPets(
            [FromQuery] string? search,
            [FromQuery] string? species,
            [FromQuery] string? gender,
            [FromQuery] int? ownerId,
            [FromQuery] string? sortBy = "newest", // newest, name_asc, age_asc, age_desc, weight_desc
            [FromQuery] int page = 1,
            [FromQuery] int pageSize = 6)
        {
            var query = _context.Pets.Include(p => p.Owner).AsQueryable();

            if (ownerId.HasValue && ownerId.Value > 0)
            {
                query = query.Where(p => p.OwnerId == ownerId.Value);
            }

            if (!string.IsNullOrWhiteSpace(search))
            {
                string kw = search.Trim().ToLower();
                query = query.Where(p => p.Name.ToLower().Contains(kw) || 
                                         p.Breed.ToLower().Contains(kw) || 
                                         p.HealthNotes.ToLower().Contains(kw));
            }

            if (!string.IsNullOrWhiteSpace(species) && species != "Tất cả")
            {
                query = query.Where(p => p.Species.ToLower() == species.Trim().ToLower());
            }

            if (!string.IsNullOrWhiteSpace(gender) && gender != "Tất cả")
            {
                query = query.Where(p => p.Gender.ToLower() == gender.Trim().ToLower());
            }

            // Sorting
            query = sortBy switch
            {
                "name_asc" => query.OrderBy(p => p.Name),
                "age_asc" => query.OrderBy(p => p.AgeYears),
                "age_desc" => query.OrderByDescending(p => p.AgeYears),
                "weight_desc" => query.OrderByDescending(p => p.WeightKg),
                _ => query.OrderByDescending(p => p.Id)
            };

            int totalItems = await query.CountAsync();
            page = Math.Max(1, page);
            pageSize = Math.Max(1, pageSize);

            var items = await query
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .Select(p => new
                {
                    p.Id,
                    p.Name,
                    p.Species,
                    p.Breed,
                    p.AgeYears,
                    p.WeightKg,
                    p.Gender,
                    p.HealthNotes,
                    p.ImageUrl,
                    p.OwnerId,
                    OwnerName = p.Owner != null ? p.Owner.FullName : "N/A",
                    p.CreatedAt
                })
                .ToListAsync();

            return Ok(new PagedResult<object>
            {
                Items = items.Cast<object>().ToList(),
                TotalItems = totalItems,
                Page = page,
                PageSize = pageSize
            });
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetPetById(int id)
        {
            var pet = await _context.Pets.Include(p => p.Owner).FirstOrDefaultAsync(p => p.Id == id);
            if (pet == null) return NotFound(new { message = "Không tìm thấy thông tin thú cưng!" });

            return Ok(new
            {
                pet.Id,
                pet.Name,
                pet.Species,
                pet.Breed,
                pet.AgeYears,
                pet.WeightKg,
                pet.Gender,
                pet.HealthNotes,
                pet.ImageUrl,
                pet.OwnerId,
                OwnerName = pet.Owner?.FullName ?? "N/A",
                pet.CreatedAt
            });
        }

        [HttpPost]
        public async Task<IActionResult> CreatePet([FromBody] Pet pet)
        {
            if (string.IsNullOrWhiteSpace(pet.Name))
            {
                return BadRequest(new { message = "Tên thú cưng không được để trống!" });
            }

            if (string.IsNullOrWhiteSpace(pet.ImageUrl))
            {
                pet.ImageUrl = pet.Species == "Mèo" 
                    ? "/images/cat_pet_1786347271937.jpg" 
                    : "/images/poodle_pet_1786347258877.jpg";
            }

            pet.CreatedAt = DateTime.UtcNow;
            _context.Pets.Add(pet);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetPetById), new { id = pet.Id }, pet);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdatePet(int id, [FromBody] Pet updatedPet)
        {
            var pet = await _context.Pets.FindAsync(id);
            if (pet == null) return NotFound(new { message = "Không tìm thấy thú cưng cần sửa!" });

            pet.Name = updatedPet.Name;
            pet.Species = updatedPet.Species;
            pet.Breed = updatedPet.Breed;
            pet.AgeYears = updatedPet.AgeYears;
            pet.WeightKg = updatedPet.WeightKg;
            pet.Gender = updatedPet.Gender;
            pet.HealthNotes = updatedPet.HealthNotes;
            if (!string.IsNullOrWhiteSpace(updatedPet.ImageUrl))
            {
                pet.ImageUrl = updatedPet.ImageUrl;
            }

            await _context.SaveChangesAsync();
            return Ok(pet);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePet(int id)
        {
            var pet = await _context.Pets.FindAsync(id);
            if (pet == null) return NotFound(new { message = "Không tìm thấy thú cưng cần xóa!" });

            _context.Pets.Remove(pet);
            await _context.SaveChangesAsync();

            return Ok(new { message = $"Đã xóa thú cưng '{pet.Name}' thành công!" });
        }
    }
}
