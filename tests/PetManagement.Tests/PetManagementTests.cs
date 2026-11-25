using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using PetManagement.Controllers;
using PetManagement.Data;
using PetManagement.Models;
using Xunit;

namespace PetManagement.Tests
{
    public class PetManagementTests
    {
        private static PetDbContext CreateContext()
        {
            var options = new DbContextOptionsBuilder<PetDbContext>()
                .UseInMemoryDatabase(databaseName: $"PetTestDb_{Guid.NewGuid()}")
                .Options;
            var context = new PetDbContext(options);
            context.Database.EnsureCreated();
            return context;
        }

        [Fact]
        public async Task ServicesApi_GetServices_ReturnsSeededActiveServices()
        {
            using var db = CreateContext();
            var controller = new ServicesApiController(db);

            var result = await controller.GetServices(null, null, "price_asc") as OkObjectResult;

            Assert.NotNull(result);
            var services = Assert.IsAssignableFrom<List<PetService>>(result!.Value);
            Assert.True(services.Count >= 4);
        }

        [Fact]
        public async Task ServicesApi_CreateUpdateAndDeleteService_WorksCorrectly()
        {
            using var db = CreateContext();
            var controller = new ServicesApiController(db);
            var newSvc = new PetService
            {
                Name = "Cắt Móng Thú Cưng",
                Category = "Spa & Grooming",
                Price = 90000,
                DurationMinutes = 15,
                Description = "Vệ sinh và mài móng an toàn",
                IsActive = true
            };

            var createRes = await controller.CreateService(newSvc) as CreatedAtActionResult;
            Assert.NotNull(createRes);

            var created = Assert.IsType<PetService>(createRes!.Value);
            created.Price = 110000;
            var updateRes = await controller.UpdateService(created.Id, created) as OkObjectResult;
            Assert.NotNull(updateRes);

            var deleteRes = await controller.DeleteService(created.Id) as OkObjectResult;
            Assert.NotNull(deleteRes);
            var svc = await db.Services.FindAsync(created.Id);
            Assert.False(svc!.IsActive);
        }

        [Fact]
        public async Task PetsApi_GetCreateUpdateAndDeletePet_WorksCorrectly()
        {
            using var db = CreateContext();
            var controller = new PetsApiController(db);

            var listRes = await controller.GetPets("Bông", "Chó", null, 2, "name_asc") as OkObjectResult;
            Assert.NotNull(listRes);

            var pet = new Pet
            {
                Name = "Milu",
                Species = "Chó",
                Breed = "Shiba Inu",
                AgeYears = 2,
                WeightKg = 9.5,
                Gender = "Đực",
                OwnerId = 2
            };

            var createdRes = await controller.CreatePet(pet) as CreatedAtActionResult;
            Assert.NotNull(createdRes);
            var createdPet = Assert.IsType<Pet>(createdRes!.Value);

            createdPet.WeightKg = 10.2;
            var updateRes = await controller.UpdatePet(createdPet.Id, createdPet) as OkObjectResult;
            Assert.NotNull(updateRes);

            var delRes = await controller.DeletePet(createdPet.Id) as OkObjectResult;
            Assert.NotNull(delRes);
        }

        [Fact]
        public async Task ProductsApi_GetCreateUpdateDeleteAndCheckout_WorksCorrectly()
        {
            using var db = CreateContext();
            var controller = new ProductsApiController(db);

            var listRes = await controller.GetProducts(null, "Thức Ăn", "price_asc") as OkObjectResult;
            Assert.NotNull(listRes);

            var newProd = new Product
            {
                Name = "Vòng Cổ Thú Cưng",
                Category = "Phụ Kiện",
                Price = 55000,
                StockQuantity = 30,
                Description = "Vòng cổ chuông nhỏ",
                Rating = 4.9
            };
            var createdProdRes = await controller.CreateProduct(newProd) as CreatedAtActionResult;
            Assert.NotNull(createdProdRes);
            var createdProd = Assert.IsType<Product>(createdProdRes!.Value);

            createdProd.Price = 60000;
            var updRes = await controller.UpdateProduct(createdProd.Id, createdProd) as OkObjectResult;
            Assert.NotNull(updRes);

            var checkoutDto = new ProductCheckoutDto
            {
                CustomerName = "Nguyễn Văn Dương",
                CustomerPhone = "0987654321",
                ShippingAddress = "Hà Nội",
                PaymentMethod = "COD",
                Items = new List<CartItemDto>
                {
                    new CartItemDto { Id = 1, Quantity = 2 }
                }
            };

            var orderRes = await controller.Checkout(checkoutDto) as OkObjectResult;
            Assert.NotNull(orderRes);

            var delProdRes = await controller.DeleteProduct(createdProd.Id) as OkObjectResult;
            Assert.NotNull(delProdRes);
        }

        [Fact]
        public async Task AppointmentsApi_GetCreateUpdateAndCancel_WorksCorrectly()
        {
            using var db = CreateContext();
            var controller = new AppointmentsApiController(db);

            var getRes = await controller.GetAppointments(2, "Completed") as OkObjectResult;
            Assert.NotNull(getRes);

            var dto = new AppointmentCreateDto
            {
                PetId = 1,
                ServiceId = 1,
                AppointmentDate = DateTime.UtcNow.AddDays(1),
                Notes = "Tắm thảo dược"
            };

            var createRes = await controller.CreateAppointment(dto, 2) as OkObjectResult;
            Assert.NotNull(createRes);

            var statusRes = await controller.UpdateStatus(1, "Confirmed") as OkObjectResult;
            Assert.NotNull(statusRes);

            var cancelRes = await controller.CancelAppointment(2) as OkObjectResult;
            Assert.NotNull(cancelRes);
        }

        [Fact]
        public async Task DashboardApi_GetStats_ReturnsAggregatedMetrics()
        {
            using var db = CreateContext();
            var controller = new DashboardApiController(db);

            var result = await controller.GetStats() as OkObjectResult;
            Assert.NotNull(result);
            Assert.NotNull(result!.Value);
        }

        [Fact]
        public async Task ContactApi_GetAndSubmitContact_WorksCorrectly()
        {
            using var db = CreateContext();
            var controller = new ContactApiController(db);

            var msg = new ContactMessage
            {
                Name = "Khách Hàng Test",
                Email = "test@petcare.com",
                Subject = "Tư vấn dịch vụ",
                Message = "Cho mình hỏi giá gói Spa?"
            };

            var postRes = await controller.SubmitContact(msg) as OkObjectResult;
            Assert.NotNull(postRes);

            var listRes = await controller.GetMessages() as OkObjectResult;
            Assert.NotNull(listRes);
        }

        [Fact]
        public async Task AuthApi_LoginRegisterOAuthAndProfile_WorksCorrectly()
        {
            using var db = CreateContext();
            var config = new ConfigurationBuilder()
                .AddInMemoryCollection(new Dictionary<string, string?>
                {
                    ["Authentication:Google:ClientId"] = "test-client-id.apps.googleusercontent.com"
                })
                .Build();

            var controller = new AuthApiController(db, config)
            {
                ControllerContext = new ControllerContext
                {
                    HttpContext = new DefaultHttpContext()
                }
            };

            var loginRes = await controller.Login(new LoginDto { Email = "admin@petcare.com", Password = "admin123" }) as OkObjectResult;
            Assert.NotNull(loginRes);

            var regRes = await controller.Register(new RegisterDto
            {
                FullName = "Nguyễn Thị Lan",
                Email = "lan@petcare.com",
                Password = "password123",
                Phone = "0912345678",
                Address = "Đà Nẵng",
                Role = "Customer"
            }) as OkObjectResult;
            Assert.NotNull(regRes);

            var oauthRes = await controller.OAuth2Login(new OAuth2LoginDto
            {
                Email = "oauth@petcare.com",
                FullName = "Google User",
                Provider = "Google"
            }) as OkObjectResult;
            Assert.NotNull(oauthRes);

            var cfgRes = controller.GetGoogleConfig() as OkObjectResult;
            Assert.NotNull(cfgRes);

            var meRes = await controller.GetCurrentUser(1) as OkObjectResult;
            Assert.NotNull(meRes);

            var notFoundMe = await controller.GetCurrentUser(9999) as NotFoundObjectResult;
            Assert.NotNull(notFoundMe);

            var badLogin = await controller.Login(new LoginDto { Email = "", Password = "" }) as BadRequestObjectResult;
            Assert.NotNull(badLogin);

            var unauthLogin = await controller.Login(new LoginDto { Email = "admin@petcare.com", Password = "wrong" }) as UnauthorizedObjectResult;
            Assert.NotNull(unauthLogin);

            var badReg = await controller.Register(new RegisterDto { Email = "", Password = "", FullName = "" }) as BadRequestObjectResult;
            Assert.NotNull(badReg);

            var dupReg = await controller.Register(new RegisterDto { Email = "admin@petcare.com", Password = "123", FullName = "Admin" }) as BadRequestObjectResult;
            Assert.NotNull(dupReg);

            var badOauth = await controller.OAuth2Login(new OAuth2LoginDto { Email = "" }) as BadRequestObjectResult;
            Assert.NotNull(badOauth);

            var badGoogle = await controller.GoogleLogin(new GoogleJwtLoginDto { IdToken = "" }) as BadRequestObjectResult;
            Assert.NotNull(badGoogle);

            var invalidGoogle = await controller.GoogleLogin(new GoogleJwtLoginDto { IdToken = "invalid.jwt.token" }) as BadRequestObjectResult;
            Assert.NotNull(invalidGoogle);

            var badSync = await controller.SyncSession(new UserDto { Id = 0, Email = "" }) as BadRequestObjectResult;
            Assert.NotNull(badSync);

            var newSync = await controller.SyncSession(new UserDto { Id = 55, FullName = "Synced User", Email = "synced@petcare.com", Role = "Customer" }) as OkObjectResult;
            Assert.NotNull(newSync);

            var existingSync = await controller.SyncSession(new UserDto { Id = 55, FullName = "Synced User", Email = "synced@petcare.com", Role = "Customer" }) as OkObjectResult;
            Assert.NotNull(existingSync);

            var byIdSync = await controller.SyncSession(new UserDto { Id = 999, FullName = "Updated Synced", Email = "", Role = "Customer" }) as OkObjectResult;
            Assert.NotNull(byIdSync);

            var logoutRes = controller.Logout() as OkObjectResult;
            Assert.NotNull(logoutRes);
        }

        [Fact]
        public async Task PetsProductsAndAppointments_EdgeCasesAndBulkDelete_WorkCorrectly()
        {
            using var db = CreateContext();
            var petsCtrl = new PetsApiController(db);
            var prodCtrl = new ProductsApiController(db);
            var apptCtrl = new AppointmentsApiController(db);
            var svcCtrl = new ServicesApiController(db);

            // Create pet with non-existent ownerId to trigger autoUser creation & fallback
            var customPet = new Pet
            {
                Name = "Ngáo Husky",
                Species = "Mèo",
                Breed = "Husky",
                AgeYears = 1,
                WeightKg = 3.5,
                Gender = "Đực",
                OwnerId = 999
            };
            var createdRes = await petsCtrl.CreatePet(customPet) as CreatedAtActionResult;
            Assert.NotNull(createdRes);
            var createdPet = Assert.IsType<Pet>(createdRes!.Value);

            // Query pets with non-existent ownerId to cover syncedUser fallback & sort options
            Assert.NotNull(await petsCtrl.GetPets(null, "Mèo", "Đực", 999, "age_asc") as OkObjectResult);
            Assert.NotNull(await petsCtrl.GetPets(null, null, null, null, "age_desc") as OkObjectResult);
            Assert.NotNull(await petsCtrl.GetPets(null, null, null, null, "weight_desc") as OkObjectResult);
            Assert.NotNull(await petsCtrl.GetPetById(createdPet.Id) as OkObjectResult);
            Assert.NotNull(await petsCtrl.GetPetById(99999) as NotFoundObjectResult);
            Assert.NotNull(await petsCtrl.CreatePet(new Pet { Name = "" }) as BadRequestObjectResult);

            // Create appointment for customPet with non-existent customerId fallback
            var apptRes = await apptCtrl.CreateAppointment(new AppointmentCreateDto
            {
                PetId = createdPet.Id,
                ServiceId = 1,
                Notes = "Test"
            }, 999) as OkObjectResult;
            Assert.NotNull(apptRes);

            Assert.NotNull(await apptCtrl.GetAppointments(999, "Tất cả") as OkObjectResult);
            Assert.NotNull(await apptCtrl.CreateAppointment(new AppointmentCreateDto { PetId = 9999, ServiceId = 9999 }, 1) as BadRequestObjectResult);

            // Bulk delete custom pets (which also cleans up related appointments)
            var bulkDel1 = await petsCtrl.DeleteCustomPets() as OkObjectResult;
            Assert.NotNull(bulkDel1);

            // Call bulk delete again when no custom pets remain
            var bulkDel2 = await petsCtrl.DeleteCustomPets() as OkObjectResult;
            Assert.NotNull(bulkDel2);

            // Delete seeded pet #1 (which has seeded appointment #1) to cover relatedAppointments cleanup in DeletePet
            var delSeedPet = await petsCtrl.DeletePet(1) as OkObjectResult;
            Assert.NotNull(delSeedPet);

            // Product & Service edge cases
            Assert.NotNull(await prodCtrl.GetProducts("Royal", "Thức Ăn", "price_desc") as OkObjectResult);
            Assert.NotNull(await prodCtrl.GetProducts(null, null, "rating_desc") as OkObjectResult);
            Assert.NotNull(await prodCtrl.GetProductById(1) as OkObjectResult);
            Assert.NotNull(await prodCtrl.GetProductById(9999) as NotFoundObjectResult);
            Assert.NotNull(await prodCtrl.CreateProduct(new Product { Name = "", Price = 0 }) as BadRequestObjectResult);
            Assert.NotNull(await prodCtrl.Checkout(new ProductCheckoutDto { Items = new List<CartItemDto>() }) as BadRequestObjectResult);
            Assert.NotNull(await prodCtrl.Checkout(new ProductCheckoutDto { Items = new List<CartItemDto> { new CartItemDto { Id = 9999, Quantity = 1 } } }) as BadRequestObjectResult);
            Assert.NotNull(await prodCtrl.Checkout(new ProductCheckoutDto { Items = new List<CartItemDto> { new CartItemDto { Id = 1, Quantity = 99999 } } }) as BadRequestObjectResult);

            Assert.NotNull(await svcCtrl.GetServices("Spa", "Spa & Grooming", "price_desc") as OkObjectResult);
            Assert.NotNull(await svcCtrl.GetServices(null, null, "name") as OkObjectResult);
            Assert.NotNull(await svcCtrl.GetServiceById(1) as OkObjectResult);
            Assert.NotNull(await svcCtrl.GetServiceById(9999) as NotFoundObjectResult);
            Assert.NotNull(await svcCtrl.CreateService(new PetService { Name = "", Price = 0 }) as BadRequestObjectResult);
        }
    }
}
