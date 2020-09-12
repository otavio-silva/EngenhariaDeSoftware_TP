using Microsoft.EntityFrameworkCore;
using REST.API.Domain.Models;

namespace REST.API.Persistance.Contexts
{
    public class AppDbContext: DbContext
    {
        public DbSet<User> Users {get; set;}
        public DbSet<Group> Groups {get; set;}
        
        public DbSet<GroupMember> GroupMembers {get; set;}
        public DbSet<Chat> Chats {get; set;}

        public DbSet<Message> Messages{get; set;}

        protected override void OnModelCreating(ModelBuilder builder) 
        {
            base.OnModelCreating(builder);

            builder.Entity<User>().ToTable("Users");
            builder.Entity<User>().HasKey(p => p.Id);
            builder.Entity<User>().Property(p => p.Id).IsRequired().ValueGeneratedOnAdd();
            builder.Entity<User>().Property(p => p.Name).IsRequired().HasMaxLength(128);
            builder.Entity<User>().Property(p => p.email).IsRequired().HasMaxLength(128);
            builder.Entity<User>().Property(p => p.password).IsRequired().HasMaxLength(32);
            builder.Entity<User>().HasMany(p => p.Messages).WithOne(p => p.Sender).HasForeignKey(p => p.SenderId);
            builder.Entity<User>().HasMany(p => p.MemberOn).WithOne(p => p.User).HasForeignKey(p => p.UserId);

            builder.Entity<Group>().ToTable("Groups");
            builder.Entity<Group>().HasKey(p => p.Id);
            builder.Entity<Group>().Property(p => p.Id).IsRequired().ValueGeneratedOnAdd();
            builder.Entity<Group>().Property(p => p.Name).HasMaxLength(128);
            builder.Entity<Group>().Property(p => p.CreatedAt).ValueGeneratedOnAdd();
            builder.Entity<Group>().HasMany(p => p.GroupMembers).WithOne(p => p.Group).HasForeignKey(p => p.GroupId);

            builder.Entity<GroupMember>().ToTable("GroupMembers");
            builder.Entity<GroupMember>().HasKey(p => p.Id);
            builder.Entity<GroupMember>().Property(p => p.Id).IsRequired().ValueGeneratedOnAdd();
            
            builder.Entity<Chat>().ToTable("Chats");
            builder.Entity<Chat>().HasKey(p => p.Id);
            builder.Entity<Chat>().Property(p => p.Id).IsRequired().ValueGeneratedOnAdd();
            builder.Entity<Chat>().Property(p => p.IsGroup).IsRequired();
            builder.Entity<Chat>().HasOne(p => p.Group).WithOne(p => p.Chat).HasForeignKey<Group>(p => p.ChatId);
            builder.Entity<Chat>().HasMany(p => p.Messages).WithOne(p => p.Chat).HasForeignKey(p => p.ChatId);

            builder.Entity<Message>().ToTable("Messages");
            builder.Entity<Message>().HasKey(p => p.Id);
            builder.Entity<Message>().Property(p => p.Id).IsRequired().ValueGeneratedOnAdd();
            builder.Entity<Message>().Property(p => p.Content).IsRequired().HasMaxLength(1024);
            builder.Entity<Message>().Property(p => p.sent_at).IsRequired().ValueGeneratedOnAdd();
            builder.Entity<Message>().Property(p => p.received_at).IsRequired(false);
            builder.Entity<Message>().Property(p => p.read_at).IsRequired(false);
        }

    }
}
