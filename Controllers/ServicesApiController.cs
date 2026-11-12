using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PetManagement.Data;
using PetManagement.Models;
using System.Linq;
using System.Threading.Tasks;

namespace PetManagement.Controllers
{
    [ApiController]
    [Route("api/services")]
    public class ServicesApiController : ControllerBase
    {
        private readonly PetDbContext _context;

        public ServicesApiController(PetDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<IActionResult> GetServices(
            [FromQuery] string? search,
            [FromQuery] string? category,
            [FromQuery] string? sortBy = "price_asc")
        {
            var query = _context.Services.Where(s => s.IsActive).AsQueryable();

            if (!string.IsNullOrWhiteSpace(search))
            {
                string kw = search.Trim().ToLower();
                query = query.Where(s => s.Name.ToLower().Contains(kw) || s.Description.ToLower().Contains(kw));
            }

            if (!string.IsNullOrWhiteSpace(category) && category != "Tất cả")
            {
                query = query.Where(s => s.Category.ToLower() == category.Trim().ToLower());
            }

            query = sortBy switch
            {
                "price_desc" => query.OrderByDescending(s => s.Price),
                "name" => query.OrderBy(s => s.Name),
                _ => query.OrderBy(s => s.Price)
            };

            var items = await query.ToListAsync();
            return Ok(items);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetServiceById(int id)
        {
            var service = await _context.Services.FindAsync(id);
            if (service == null) return NotFound(new { message = "Không tìm thấy dịch vụ!" });
            return Ok(service);
        }

        [HttpPost]
        public async Task<IActionResult> CreateService([FromBody] PetService service)
        {
            if (string.IsNullOrWhiteSpace(service.Name) || service.Price <= 0)
            {
                return BadRequest(new { message = "Tên dịch vụ và giá hợp lệ là bắt buộc!" });
            }

            _context.Services.Add(service);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetServiceById), new { id = service.Id }, service);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateService(int id, [FromBody] PetService updatedService)
        {
            var service = await _context.Services.FindAsync(id);
            if (service == null) return NotFound(new { message = "Không tìm thấy dịch vụ!" });

            service.Name = updatedService.Name;
            service.Category = updatedService.Category;
            service.Price = updatedService.Price;
            service.DurationMinutes = updatedService.DurationMinutes;
            service.Description = updatedService.Description;
            if (!string.IsNullOrWhiteSpace(updatedService.ImageUrl))
            {
                service.ImageUrl = updatedService.ImageUrl;
            }
            service.IsActive = updatedService.IsActive;

            await _context.SaveChangesAsync();
            return Ok(service);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteService(int id)
        {
            var service = await _context.Services.FindAsync(id);
            if (service == null) return NotFound(new { message = "Không tìm thấy dịch vụ!" });

            service.IsActive = false; // Soft delete
            await _context.SaveChangesAsync();

            return Ok(new { message = $"Đã ngưng cung cấp dịch vụ '{service.Name}'." });
        }
    }
}
