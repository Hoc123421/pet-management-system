using Microsoft.EntityFrameworkCore;
using PetManagement.Models;
using System;
using System.Collections.Generic;

namespace PetManagement.Data
{
    public class PetDbContext : DbContext
    {
        public PetDbContext(DbContextOptions<PetDbContext> options) : base(options)
        {
        }

        public DbSet<User> Users { get; set; } = null!;
        public DbSet<Pet> Pets { get; set; } = null!;
        public DbSet<PetService> Services { get; set; } = null!;
        public DbSet<Appointment> Appointments { get; set; } = null!;
        public DbSet<Product> Products { get; set; } = null!;
        public DbSet<ProductOrder> ProductOrders { get; set; } = null!;
        public DbSet<ContactMessage> ContactMessages { get; set; } = null!;


        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // User - Pet relationship
            modelBuilder.Entity<Pet>()
                .HasOne(p => p.Owner)
                .WithMany(u => u.Pets)
                .HasForeignKey(p => p.OwnerId)
                .OnDelete(DeleteBehavior.Cascade);

            // Appointment relationships
            modelBuilder.Entity<Appointment>()
                .HasOne(a => a.Pet)
                .WithMany(p => p.Appointments)
                .HasForeignKey(a => a.PetId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<Appointment>()
                .HasOne(a => a.Service)
                .WithMany(s => s.Appointments)
                .HasForeignKey(a => a.ServiceId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<Appointment>()
                .HasOne(a => a.Customer)
                .WithMany(u => u.Appointments)
                .HasForeignKey(a => a.CustomerId)
                .OnDelete(DeleteBehavior.Cascade);

            // Seed Users
            modelBuilder.Entity<User>().HasData(
                new User
                {
                    Id = 1,
                    FullName = "Quản Trị Viên (Admin)",
                    Email = "admin@petcare.com",
                    PasswordHash = "admin123", // Simple hash for demo project
                    Role = "Admin",
                    Phone = "0901234567",
                    Address = "123 Nguyễn Trãi, TP. Hà Nội",
                    AvatarUrl = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&auto=format&fit=crop",
                    OAuthProvider = "Local"
                },
                new User
                {
                    Id = 2,
                    FullName = "Nguyễn Văn Dương",
                    Email = "duongnguyen@gmail.com",
                    PasswordHash = "user123",
                    Role = "Customer",
                    Phone = "0987654321",
                    Address = "456 Nguyễn Trãi, TP. Hà Nội",
                    AvatarUrl = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&auto=format&fit=crop",
                    OAuthProvider = "Local"
                }
            );

            // Seed Pet Services
            modelBuilder.Entity<PetService>().HasData(
                new PetService
                {
                    Id = 1,
                    Name = "Spa & Cắt Tỉa Lông Toàn Diện",
                    Category = "Spa & Grooming",
                    Price = 350000,
                    DurationMinutes = 60,
                    Description = "Tắm spa thảo dược, cắt tỉa lông tạo kiểu nghệ thuật, vệ sinh tai và cắt móng cao cấp.",
                    ImageUrl = "https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=600&auto=format&fit=crop",
                    IsActive = true
                },
                new PetService
                {
                    Id = 2,
                    Name = "Khám Sức Khỏe Tổng Quát & Tiêm Phòng",
                    Category = "Khám Sức Khỏe",
                    Price = 250000,
                    DurationMinutes = 30,
                    Description = "Khám tim phổi, soi da tai móng, tư vấn dinh dưỡng và tiêm vắc-xin phòng bệnh 7 trong 1.",
                    ImageUrl = "https://images.unsplash.com/photo-1628009368231-7bb7cfcb0def?w=600&auto=format&fit=crop",
                    IsActive = true
                },
                new PetService
                {
                    Id = 3,
                    Name = "Khách Sạn Thú Cưng VIP (1 Đêm)",
                    Category = "Khách Sạn Thú Cưng",
                    Price = 300000,
                    DurationMinutes = 1440,
                    Description = "Phòng máy lạnh riêng biệt, camera theo dõi 24/7, 3 bữa ăn dinh dưỡng và 2 lượt dạo chơi mỗi ngày.",
                    ImageUrl = "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=600&auto=format&fit=crop",
                    IsActive = true
                },
                new PetService
                {
                    Id = 4,
                    Name = "Tẩy Giun & Vệ Sinh Răng Miệng",
                    Category = "Khám Sức Khỏe",
                    Price = 180000,
                    DurationMinutes = 25,
                    Description = "Lấy cao răng siêu âm nhẹ nhàng, uống thuốc tẩy giun định kỳ và xịt thơm miệng.",
                    ImageUrl = "https://images.unsplash.com/photo-1548767797-d8c844163c4c?w=600&auto=format&fit=crop",
                    IsActive = true
                }
            );

            // Seed Pets
            modelBuilder.Entity<Pet>().HasData(
                new Pet
                {
                    Id = 1,
                    Name = "Bé Bông",
                    Species = "Chó",
                    Breed = "Poodle Bò Sữa",
                    AgeYears = 2,
                    WeightKg = 4.5,
                    Gender = "Cái",
                    HealthNotes = "Rất ngoan, thích ăn thịt gà, đã tiêm đủ 3 mũi vắc-xin.",
                    ImageUrl = "/images/poodle_pet_1786347258877.jpg",
                    OwnerId = 2
                },
                new Pet
                {
                    Id = 2,
                    Name = "Miu Miu",
                    Species = "Mèo",
                    Breed = "Mèo Anh Lông Ngắn",
                    AgeYears = 1,
                    WeightKg = 3.8,
                    Gender = "Đực",
                    HealthNotes = "Lông mềm mịn, hơi nhát người lạ, thích chải lông.",
                    ImageUrl = "/images/cat_pet_1786347271937.jpg",
                    OwnerId = 2
                },
                new Pet
                {
                    Id = 3,
                    Name = "Mochi",
                    Species = "Chó",
                    Breed = "Corgi Pembroke",
                    AgeYears = 3,
                    WeightKg = 11.2,
                    Gender = "Đực",
                    HealthNotes = "Năng động, thích chạy nhảy, tai dựng đẹp.",
                    ImageUrl = "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=600&auto=format&fit=crop",
                    OwnerId = 1
                },
                new Pet
                {
                    Id = 4,
                    Name = "Loki",
                    Species = "Chó",
                    Breed = "Golden Retriever",
                    AgeYears = 4,
                    WeightKg = 28.0,
                    Gender = "Đực",
                    HealthNotes = "Thân thiện, biết làm xiếc, sức khỏe rất tốt.",
                    ImageUrl = "/images/pet_hero_banner_1786347242679.jpg",
                    OwnerId = 1
                }
            );

            // Seed Products
            modelBuilder.Entity<Product>().HasData(
                new Product
                {
                    Id = 1,
                    Name = "Hạt Dinh Dưỡng Royal Canin Poodle (1.5kg)",
                    Category = "Thức Ăn",
                    Price = 285000,
                    StockQuantity = 45,
                    Description = "Thức ăn cao cấp chăm sóc bộ lông xoăn mịn đặc trưng của giống chó Poodle.",
                    ImageUrl = "https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600&auto=format&fit=crop",
                    Rating = 4.9
                },
                new Product
                {
                    Id = 2,
                    Name = "Pate Mèo Snappy Tom Vị Cá Hồi & Gà (400g)",
                    Category = "Thức Ăn",
                    Price = 45000,
                    StockQuantity = 120,
                    Description = "Pate nguyên chất giàu Protein, Omega 3 & 6 giúp mèo sáng mắt và mượt lông.",
                    ImageUrl = "https://images.unsplash.com/photo-1548767797-d8c844163c4c?w=600&auto=format&fit=crop",
                    Rating = 4.8
                },

                new Product
                {
                    Id = 3,
                    Name = "Cần Câu Mèo Gắn Lông Vũ & Chuông Tương Tác",
                    Category = "Đồ Chơi",
                    Price = 65000,
                    StockQuantity = 80,
                    Description = "Đồ chơi tương tác giúp mèo vận động xả stress, tay cầm dẻo bền bỉ.",
                    ImageUrl = "https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=600&auto=format&fit=crop",
                    Rating = 4.7
                },
                new Product
                {
                    Id = 4,
                    Name = "Sữa Tắm Thảo Dược Trị Ve Rận JoyPet (500ml)",
                    Category = "Sức Khỏe",
                    Price = 195000,
                    StockQuantity = 35,
                    Description = "Chiết xuất tinh dầu tự nhiên khử mùi hôi, diệt ve rận và lưu hương dịu nhẹ 7 ngày.",
                    ImageUrl = "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600&auto=format&fit=crop",
                    Rating = 5.0
                },
                new Product
                {
                    Id = 5,
                    Name = "Khay Đựng Thức Ăn Đôi Chống Trượt Inox",
                    Category = "Phụ Kiện",
                    Price = 150000,
                    StockQuantity = 50,
                    Description = "Bát đôi inox cao cấp chống rỉ, chân đế cao su chống trượt giúp thú cưng ăn uống thoải mái.",
                    ImageUrl = "https://images.unsplash.com/photo-1541599540903-216a46ca1dc0?w=600&auto=format&fit=crop",
                    Rating = 4.8
                }
            );


            // Seed Appointments
            modelBuilder.Entity<Appointment>().HasData(
                new Appointment
                {
                    Id = 1,
                    PetId = 1,
                    ServiceId = 1,
                    CustomerId = 2,
                    AppointmentDate = DateTime.UtcNow.AddDays(-2),
                    Status = "Completed",
                    Notes = "Cắt tỉa theo phong cách Teddy Bear.",
                    TotalPrice = 350000,
                    CreatedAt = DateTime.UtcNow.AddDays(-3)
                },
                new Appointment
                {
                    Id = 2,
                    PetId = 2,
                    ServiceId = 2,
                    CustomerId = 2,
                    AppointmentDate = DateTime.UtcNow.AddDays(-1),
                    Status = "Completed",
                    Notes = "Khám tai và kiểm tra cân nặng.",
                    TotalPrice = 250000,
                    CreatedAt = DateTime.UtcNow.AddDays(-2)
                }
            );

        }
    }
}
