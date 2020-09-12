using System;
using System.Collections.Generic;

namespace REST.API.Domain.Models
{
    public class Group
    {
        public int Id {get; set;}
        public string Name {get; set;}
        public DateTime CreatedAt {get; set;}

        public int ChatId {get; set;}
        public Chat Chat {get; set;}
        public IList<GroupMember> GroupMembers {get; set;} = new List<GroupMember>();
    }
}