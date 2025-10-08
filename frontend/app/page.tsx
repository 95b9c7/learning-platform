import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  Shield, 
  Users, 
  Award, 
  Clock, 
  Star,
  ArrowRight,
  CheckCircle,
  PlayCircle
} from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4">
        <div className="container mx-auto text-center">
          <Badge variant="secondary" className="mb-6 pulse-glow">
            <Shield className="w-4 h-4 mr-2" />
            OSHA & DOT Compliant Training
          </Badge>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 gradient-text">
            Professional Operator Safety Training
          </h1>
          
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto">
            Master essential safety skills with industry-leading courses designed for commercial drivers, 
            equipment operators, and safety professionals. Stay compliant, stay safe.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/courses">
              <Button size="lg" className="btn-primary pulse-glow">
                Browse Safety Courses
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/about">
              <Button size="lg" variant="outline" className="hover:bg-primary/10 hover:text-primary hover:border-primary">
                Learn More
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold gradient-text mb-2">500+</div>
              <div className="text-muted-foreground">Safety Courses</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold gradient-text mb-2">50K+</div>
              <div className="text-muted-foreground">Operators Trained</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold gradient-text mb-2">99.8%</div>
              <div className="text-muted-foreground">Pass Rate</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold gradient-text mb-2">24/7</div>
              <div className="text-muted-foreground">Support</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
              Why Choose SafeOperator Pro?
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Industry-leading safety training platform trusted by thousands of operators nationwide.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="card-enhanced">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Shield className="w-8 h-8 text-primary" />
                </div>
                <h3 className="text-2xl font-bold mb-4">OSHA Compliant</h3>
                <p className="text-muted-foreground">
                  All courses meet OSHA standards and industry best practices for maximum safety compliance.
                </p>
              </CardContent>
            </Card>
            
            <Card className="card-enhanced">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Users className="w-8 h-8 text-accent" />
                </div>
                <h3 className="text-2xl font-bold mb-4">Expert Instructors</h3>
                <p className="text-muted-foreground">
                  Learn from certified safety professionals with decades of real-world experience.
                </p>
              </CardContent>
            </Card>
            
            <Card className="card-enhanced">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Award className="w-8 h-8 text-secondary-foreground" />
                </div>
                <h3 className="text-2xl font-bold mb-4">Certification Ready</h3>
                <p className="text-muted-foreground">
                  Earn recognized certifications that advance your career and ensure workplace safety.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Popular Courses Preview */}
      <section className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
              Popular Safety Courses
            </h2>
            <p className="text-xl text-muted-foreground">
              Start with these essential safety training programs.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="card-enhanced">
              <CardContent className="p-6">
                <div className="flex items-center gap-3 mb-4">
                  <PlayCircle className="w-6 h-6 text-primary" />
                  <Badge variant="secondary">Equipment Safety</Badge>
                </div>
                <h3 className="text-xl font-bold mb-2">Forklift Operator Safety</h3>
                <p className="text-muted-foreground mb-4">
                  Master forklift operation with comprehensive safety protocols and hands-on training.
                </p>
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    <span>8 hours</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Star className="w-4 h-4 fill-yellow-500 text-yellow-500" />
                    <span>4.9</span>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="card-enhanced">
              <CardContent className="p-6">
                <div className="flex items-center gap-3 mb-4">
                  <PlayCircle className="w-6 h-6 text-accent" />
                  <Badge variant="secondary">Commercial Driving</Badge>
                </div>
                <h3 className="text-xl font-bold mb-2">CDL Hazmat Training</h3>
                <p className="text-muted-foreground mb-4">
                  Specialized training for handling hazardous materials safely and legally.
                </p>
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    <span>12 hours</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Star className="w-4 h-4 fill-yellow-500 text-yellow-500" />
                    <span>4.8</span>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="card-enhanced">
              <CardContent className="p-6">
                <div className="flex items-center gap-3 mb-4">
                  <PlayCircle className="w-6 h-6 text-secondary-foreground" />
                  <Badge variant="secondary">Workplace Safety</Badge>
                </div>
                <h3 className="text-xl font-bold mb-2">Confined Space Entry</h3>
                <p className="text-muted-foreground mb-4">
                  Learn critical safety procedures for confined space operations and rescue.
                </p>
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    <span>6 hours</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Star className="w-4 h-4 fill-yellow-500 text-yellow-500" />
                    <span>4.9</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
          
          <div className="text-center mt-12">
            <Link href="/courses">
              <Button size="lg" className="btn-primary">
                View All Courses
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
            Ready to Start Your Safety Training?
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of operators who trust SafeOperator Pro for their safety training needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="btn-primary pulse-glow">
                Get Started Today
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/contact">
              <Button size="lg" variant="outline" className="hover:bg-primary/10 hover:text-primary hover:border-primary">
                Contact Us
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
