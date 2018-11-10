#!/usr/bin/perl -w
#clinical_xml2tbl.pl

#export PERL5LIB=/project/BICF/BICF_Core/s166458/seqprg/lib/perl5/:$PERL5LIB
use File::Slurper 'read_text';
use XML::Simple qw(:strict);
$xml = new XML::Simple;

my %otree;
my %diags;
my $header =<ONCOTREE>;
open ONCOTREE, "<Unique_Synonyms.csv" or die $!;
while (my $line = <ONCOTREE>) {
    chomp($line);
    my ($num,$oncocode,$diagnosis) = split(/,/,$line);
    push @{$otree{$oncocode}}, $diagnosis;
    $diag{$diagnosis} = $oncocode;
}
open DIAG, "<diagnosis.txt" or die $!;
my $head = <DIAG>;
while (my $line = <DIAG>) {
    chomp($line);
    my ($oncocode,$diagnosis) = split(/\t/,$line);
    $diagnosis =~ s/\"//g;
    push @{$otree{$oncocode}}, $diagnosis;
}

my @xmlfiles = `ls /project/hackathon/hackers11/shared/NCTxml/*.xml`;
chomp(@xmlfiles);
open OUT, ">clinicaltrialdb.txt" or die $!;
print OUT join("\t",'NCT','Phase','Conditions','Drugs','BriefTitle','OfficialTrial','Oncotree Codes'),"\n";

$total = 0;
$match = 0;

foreach $file (@xmlfiles) {
    $total ++;
    my $study = $xml->XMLin($file,forcearray => [qw(arm_group condition mesh_term intervention intervention_browse location keyword location_countries secondary_outcome)],keyattr => []);
    $brief_title= $study->{brief_title};
    $official_title= $study->{official_title};
    @conditions= @{$study->{condition}};
    my %oncotree;
  F1:foreach $cond (@conditions) {
      if ($diag{$cond}) {
	  $oncotree{$diag{$cond}} = 1;
	  next F1;
      }
      foreach $ocode (keys %otree) {
	  foreach $diag (@{$otree{$ocode}}) {
	      if ($diag =~ m/$cond/i) {
		  $oncotree{$ocode} = 1 if (length($ocode) > 1) ;
	      }elsif ($cond =~ m/$diag/i) {
		  $oncotree{$ocode} = 1 if (length($ocode) > 1) ;
	      }
	  }
      }
  }
    my @oncotreecodes = keys %oncotree;
    $match ++ if ($#oncotreecodes > 0);
    
    $phase= $study->{phase};
    $phase =~ s/Phase //i;
    $nct_number = $study->{'id_info'}->{nct_id};
    my @drugs;
    foreach $intr (@{$study->{intervention}}) {
	push @drugs, $intr->{intervention_name} if  $intr->{intervention_type} =~ m/drug/i;
    }
    print OUT join("\t",$nct_number,$phase,join("|",@conditions),join("|",@drugs),$brief_title,$official_title,join("|",keys %oncotree)),"\n";
}
