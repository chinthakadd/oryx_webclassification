import Orange

data = Orange.data.Table("dataset.csv")
print "Attributes:", ", ".join(x.name for x in data.domain.features)
print "Class:", data.domain.class_var.name
print "Data instances", len(data)

target = "Blogs"
print "Data instances with %s type:" % target
for d in data:
    if d.get_class() == target:
        print " ".join(["%-15s" % str(v) for v in d])


data.save("new_data.tab")        