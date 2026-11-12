using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PetManagement.Data;
using PetManagement.Models;
using System.Linq;
using System.Threading.Tasks;

namespace PetManagement.Controllers
{
    [ApiController]
    [Route("api/products")]
    public class ProductsApiController : ControllerBase
    {
        private readonly PetDbContext _context;

        public ProductsApiController(PetDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<IActionResult> GetProducts(
            [FromQuery] string? search,
            [FromQuery] string? category,
            [FromQuery] string? sortBy = "newest", // newest, price_asc, price_desc, rating_desc
            [FromQuery] int page = 1,
            [FromQuery] int pageSize = 8)
        {
            var query = _context.Products.AsQueryable();

            if (!string.IsNullOrWhiteSpace(search))
            {
                string kw = search.Trim().ToLower();
                query = query.Where(p => p.Name.ToLower().Contains(kw) || p.Description.ToLower().Contains(kw));
            }

            if (!string.IsNullOrWhiteSpace(category) && category != "Tất cả")
            {
                query = query.Where(p => p.Category.ToLower() == category.Trim().ToLower());
            }

            query = sortBy switch
            {
                "price_asc" => query.OrderBy(p => p.Price),
                "price_desc" => query.OrderByDescending(p => p.Price),
                "rating_desc" => query.OrderByDescending(p => p.Rating),
                _ => query.OrderByDescending(p => p.Id)
            };

            int totalItems = await query.CountAsync();
            page = Math.Max(1, page);
            pageSize = Math.Max(1, pageSize);

            var items = await query
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return Ok(new PagedResult<Product>
            {
                Items = items,
                TotalItems = totalItems,
                Page = page,
                PageSize = pageSize
            });
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetProductById(int id)
        {
            var product = await _context.Products.FindAsync(id);
            if (product == null) return NotFound(new { message = "Không tìm thấy sản phẩm!" });
            return Ok(product);
        }

        [HttpPost]
        public async Task<IActionResult> CreateProduct([FromBody] Product product)
        {
            if (string.IsNullOrWhiteSpace(product.Name) || product.Price <= 0)
            {
                return BadRequest(new { message = "Tên sản phẩm và Giá bán hợp lệ là bắt buộc!" });
            }

            _context.Products.Add(product);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetProductById), new { id = product.Id }, product);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateProduct(int id, [FromBody] Product updatedProduct)
        {
            var product = await _context.Products.FindAsync(id);
            if (product == null) return NotFound(new { message = "Không tìm thấy sản phẩm!" });

            product.Name = updatedProduct.Name;
            product.Category = updatedProduct.Category;
            product.Price = updatedProduct.Price;
            product.StockQuantity = updatedProduct.StockQuantity;
            product.Description = updatedProduct.Description;
            if (!string.IsNullOrWhiteSpace(updatedProduct.ImageUrl))
            {
                product.ImageUrl = updatedProduct.ImageUrl;
            }
            product.Rating = updatedProduct.Rating;

            await _context.SaveChangesAsync();
            return Ok(product);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteProduct(int id)
        {
            var product = await _context.Products.FindAsync(id);
            if (product == null) return NotFound(new { message = "Không tìm thấy sản phẩm!" });

            _context.Products.Remove(product);
            await _context.SaveChangesAsync();

            return Ok(new { message = $"Đã xóa sản phẩm '{product.Name}'!" });
        }

        [HttpPost("checkout")]
        public async Task<IActionResult> Checkout([FromBody] ProductCheckoutDto dto)
        {
            if (dto == null || dto.Items == null || dto.Items.Count == 0)
            {
                return BadRequest(new { message = "Giỏ hàng của bạn đang trống!" });
            }

            decimal totalAmount = 0;

            foreach (var item in dto.Items)
            {
                var product = await _context.Products.FindAsync(item.Id);
                if (product != null)
                {
                    int qty = Math.Max(1, item.Quantity);
                    product.StockQuantity = Math.Max(0, product.StockQuantity - qty);
                    totalAmount += product.Price * qty;
                }
            }

            var order = new ProductOrder
            {
                CustomerName = dto.CustomerName,
                CustomerPhone = dto.CustomerPhone,
                ShippingAddress = dto.ShippingAddress,
                PaymentMethod = dto.PaymentMethod,
                TotalAmount = totalAmount,
                Status = "Completed",
                CreatedAt = DateTime.UtcNow
            };

            _context.ProductOrders.Add(order);
            await _context.SaveChangesAsync();

            return Ok(new { message = "Thanh toán đơn hàng thành công!", orderId = order.Id, totalAmount = totalAmount });
        }
    }
}

